import os
import yaml
import json

import rasterio
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

from download_from_cdse import query_id
from spectral_index import apply_ndvi
from preprocess import digital_numbers_to_reflectance
from utils import dates_to_days

if __name__ == "__main__":
    with open('cdse_query.yaml', 'r') as file:
        query = yaml.safe_load(file)

    bands = query['bands']
    data_folder = os.path.join(query['data_folder'], query_id(query, temporal_id=False))
    years = sorted(os.listdir(data_folder))

    train_data_folder = os.path.join(data_folder, years[0])

    # Load Sentinel-2 data
    with open(os.path.join(train_data_folder, bands[0], 'job-results.json'), 'r') as f:
        job_results = json.load(f)

    img_files = list(job_results['assets'].keys())
    img_dates = [file.split('_')[-1].split('Z')[0] for file in img_files]

    # Make Sentinel-2 time series
    train_ts = {}
    for date in img_dates:
        train_ts[date] = dict((
            band, 
            rasterio.open(os.path.join(train_data_folder, band, f'SENTINEL2_L2A_{band}_{date}Z.tif'))) 
            for band in bands)
        train_ts[date]['NDVI'] = apply_ndvi(train_ts[date], preprocess=digital_numbers_to_reflectance)
        # train_ts[date]['RGB'] = ...

    dates = np.array(list(train_ts.keys()))
    n_dates = len(dates)
    days = dates_to_days(np.array([datetime.strptime(date, '%Y-%m-%d') for date in train_ts]))
  
    # Make a raster of size (n_days, height, width) of NDVI
    ndvi_array = np.array([train_ts[date]['NDVI'] for date in train_ts])
    height, width = ndvi_array.shape[1], ndvi_array.shape[2]
    px_coords = height // 2, width // 2

    # Plot the NDVI time series    
    fig, ax = plt.subplots()
    fontsize = 15
    ndvi_px = ndvi_array[:, px_coords[0], px_coords[1]]
    ax.scatter(days, ndvi_px, color="#8fc0a9")
    ax.set_ylabel("NDVI", fontsize=fontsize)
    ax.set_ylim([-1, 1])
    xticks = np.arange(len(dates))[::6]
    xticklabels = dates[xticks]
    ax.set_xticks(days[xticks], labels=xticklabels, rotation=45)
    ax.xaxis.grid(True, which="major", linestyle="dashed")
    plt.show()

    # Plot RGB composition over the time series
    # n_rows, n_cols = 2, 4
    # figsize = (150, 150)
    # for i in range(n_dates // (n_rows * n_cols)):    
    #     fig, axs = plt.subplots(n_rows, n_cols, figsize=figsize)
    #     for i, (ax, date) in enumerate(zip(axs.flat, dates[i*n_rows*n_cols:(i+1)*n_rows*n_cols])):
    #         ax.imshow(train_ts[date]['RGB'])
    #         ax.set_xticks([])
    #         ax.set_yticks([])
    #         ax.set_title(date)
    #     plt.show()