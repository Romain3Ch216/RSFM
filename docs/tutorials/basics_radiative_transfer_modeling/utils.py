import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, List, Tuple


def palette():
    return {
        'black': '#272838',
        'yellow': '#f3de8a',
        'red': '#eb9486',
        'gray': '#7e7f9a',
        'purple': '#a288e3'
    }

def rgb_render(
    data: np.ndarray,
    clip: int = 2,
    bands: Optional[List[int]] = None,
    norm: bool = True,
    dmin: Optional[np.ndarray] = None,
    dmax: Optional[np.ndarray] = None
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
    # If normalization is on
    if norm:
        # Rescale and clip data according to percentile
        if dmin is None:
            out_dmin = np.nanpercentile(data_ready, clip, axis=(1, 2))
        else:
            out_dmin = dmin
        if dmax is None:
            out_dmax = np.nanpercentile(data_ready, 100 - clip, axis=(1, 2))
        else:
            out_dmax = dmax
        data_ready = np.clip((data_ready.transpose(1, 2, 0) - out_dmin) / (out_dmax - out_dmin), 0, 1)

    else:
        data_ready.transpose(1, 2, 0)

    # Strip of one dimension if number of bands is 1
    if data_ready.shape[-1] == 1:
        data_ready = data_ready[:, :, 0]

    return data_ready, out_dmin, out_dmax


def plot_dict(d: dict, title="Dictionary structure"):
    """Plot dict keys and their value types as a styled table (Jupyter-friendly)."""
    df = pd.DataFrame(
        [{"key": k, "type": type(v).__name__, "value_preview": repr(v)[:50]}
         for k, v in d.items()]
    ).set_index("key")

    return df
