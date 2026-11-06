from typing import Dict, Callable


def apply_ndvi(raster_dst: Dict, preprocess: Callable = lambda x: x, eps: float = 1e-4):
    """Normalized Difference Vegetation Index.
    Formula for Sentinel-2 bands: (B08-B04)/(B08+B04)

    Args:
        rasters: dictionary with keys B01, ..., B12 mapping to rasterio.io.DatasetReader datasets

    Returns:
        an array of NDVI values.
    """
    raise NotImplementedError