import os
import yaml
import json

import rasterio
import matplotlib.pyplot as plt

from download_from_cdse import query_id


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

    # Plot the time series
    n_rows, n_cols = 2, 4
    figsize = (150, 150)
    dates = list(train_ts.keys())
    n_dates = len(img_dates)
    for i in range(n_dates // (n_rows * n_cols)):    
        fig, axs = plt.subplots(n_rows, n_cols, figsize=figsize)
        for i, (ax, date) in enumerate(zip(axs.flat, dates[i*n_rows*n_cols:(i+1)*n_rows*n_cols])):
            ax.imshow(train_ts[date]['RGB'])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(date)
        plt.show()