import numpy as np
from typing import Optional, List, Tuple
from datetime import datetime
from rasterio.features import shapes
from rasterio.transform import from_bounds
import shapefile


def rgb_render(
    data: np.ndarray,
    clip: int = 2,
    bands: Optional[List[int]] = None,
    norm: bool = True,
    dmin: Optional[np.ndarray] = None,
    dmax: Optional[np.ndarray] = None,
    mask: Optional[np.ndarray] = None
) -> Tuple[np.ndarray, Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Prepare data for visualization with matplot lib, taken (with minor modifications) from the sensorsio repo by Julien Michel
    Source: https://framagit.org/jmichel-otb/sensorsio/-/blob/master/src/sensorsio/utils.py?ref_type=heads
    License: Apache License, Version 2.0

    :param data: nd_array of shape [bands, w, h]
    :param clip: clip percentile (between 0 and 100). Ignored if norm is False
    :bands: List of bands to extract (len is 1 or 3 for RGB)
    :norm: If true, clip a percentile at each end

    :returns: a tuple of data ready for matplotlib, dmin, dmax
    """
    if bands is None:
        bands = [2, 1, 0]
    assert len(bands) == 1 or len(bands) == 3
    assert 0 <= clip <= 100

    # Extract bands from data
    data_ready = np.take(data, bands, axis=0)
    out_dmin = None
    out_dmax = None

    data_for_stat = np.copy(data_ready)
    if mask is not None:
        data_for_stat[:, mask] = np.nan

    # If normalization is on
    if norm:
        # Rescale and clip data according to percentile
        if dmin is None:
            out_dmin = np.nanpercentile(data_for_stat, clip, axis=(1, 2))
        else:
            out_dmin = dmin
        if dmax is None:
            out_dmax = np.nanpercentile(data_for_stat, 100 - clip, axis=(1, 2))
        else:
            out_dmax = dmax
        if np.isnan(out_dmin).any() or np.isnan(out_dmax).any():
            data_ready = data_ready.transpose(1, 2, 0)
        else:
            data_ready = np.clip((data_ready.transpose(1, 2, 0) - out_dmin) / (out_dmax - out_dmin), 0, 1)

    else:
        data_ready = data_ready.transpose(1, 2, 0)

    # Strip of one dimension if number of bands is 1
    if data_ready.shape[-1] == 1:
        data_ready = data_ready[:, :, 0]

    return data_ready, out_dmin, out_dmax


def dates_to_days(dates, ref_day: str = '2015-01-01'):
    """
    Converts datetime objects to days since reference date.

    Parameters
    ----------
    dates : array-like of datetime-like
        Input dates to convert.

    Returns
    -------
    numpy.ndarray
        Array of integers representing days since ref_day (2015-01-01).
    """
    ref_day = datetime.strptime(ref_day, '%Y-%m-%d')
    try:
        days = (dates - ref_day).astype("timedelta64[D]").astype(int)
    except ValueError as e:
        # .astype("timedelta64[D]") not supported anymore by pandas series
        # https://stackoverflow.com/a/76363956
        # https://github.com/pandas-dev/pandas/blob/8cf4ab491b06274f555d1ea305c172354208747a/doc/source/whatsnew/v2.0.0.rst#disallow-astype-conversion-to-non-supported-datetime64timedelta64-dtypes
        pd_msg = "Supported resolutions are 's', 'ms', 'us', 'ns'"
        if pd_msg in str(e):
            days = (dates - ref_day).days
        else:
            raise e

    return days


def binary_array_to_polygons(array, top_left, bottom_right, out_path):
    """Merge contiguous pixels == 1 into single polygons."""
    array = np.asarray(array).astype(np.uint8)
    rows, cols = array.shape

    lat_top, lon_left = top_left
    lat_bottom, lon_right = bottom_right

    # Affine transform: same convention as before (row 0 = northernmost)
    transform = from_bounds(
        west=lon_left, south=lat_bottom,
        east=lon_right, north=lat_top,
        width=cols, height=rows,
    )

    # Generator of (geometry, value) for each contiguous region
    mask = array == 1
    results = shapes(array, mask=mask, transform=transform, connectivity=8)

    shp = shapefile.Writer(out_path, shapeType=shapefile.POLYGON)
    shp.field("Value", "N", decimal=0)
    try:
        for geom, value in results:
            # geom is GeoJSON-like: {"type": "Polygon"/"MultiPolygon", "coordinates": ...}
            if geom["type"] == "Polygon":
                parts = geom["coordinates"]          # [ring, hole, hole...]
                rings = [[(x, y) for x, y in ring] for ring in parts]
                shp.poly(rings)
                shp.record(int(value))
            else:  # MultiPolygon
                for poly in geom["coordinates"]:
                    rings = [[(x, y) for x, y in ring] for ring in poly]
                    shp.poly(rings)
                    shp.record(int(value))
    finally:
        shp.close()

    wgs84 = ('GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
             'SPHEROID["WGS_1984",6378137,298.257223563]],'
             'PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]]')
    with open(out_path + ".prj", "w") as f:
        f.write(wgs84)

    print(f"Fichier créé : {out_path}.shp")
