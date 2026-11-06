from typing import Dict, Callable

import numpy as np
import rasterio

from utils import rgb_render


def digital_numbers_to_reflectance(raster: np.ndarray):
    """Convert a Sentinel-2 raster provided in digital numbers to reflectance
    for data acquired from 2016 to 2020. In this period, the formula for every
    S2 bands is : REFLECTANCE = DIGITAL_NUMBERS / 10000.
    """
    raster = raster / 10000
    raster = np.clip(raster, a_min=0, a_max=None)
    return raster


def apply_cloud_mask(
    rasters: Dict[str, rasterio.io.DatasetReader], 
    preprocess: Callable = lambda x: x, 
    ):
    """Cloud mask.
    
    Args:
        rasters: dictionary with keys B01, ..., B12 mapping to rasterio.io.DatasetReader datasets
        preprocess: optional argument, e.g. to convert Digital Numbers in reflectance
    """
    raise NotImplementedError


def apply_rgb_compo(
    rasters: Dict[str, rasterio.io.DatasetReader], 
    preprocess: Callable = lambda x: x, 
    mask: np.ndarray = None,
    render: bool = True):
    """Make a RGB composition from multispectral data.

    Args:
        rasters: dictionary with keys B01, ..., B12 mapping to rasterio.io.DatasetReader datasets
        preprocess: optional argument, e.g. to convert Digital Numbers in reflectance
        mask: boolean array of invalid pixels (True = invalid)
        render: if True, return an uint8 array stretched for display;
            if False, return the raw composition.
    """
    raise NotImplementedError