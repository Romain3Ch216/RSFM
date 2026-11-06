"""Download Copernicus data from the Copernicus Data Space Ecosystem (https://documentation.dataspace.copernicus.eu/Home.html)
using the Open EO API (https://openeo.org/).

The queried Copernicus collection (e.g. Sentinel-2 L2A) and spatial / temporal / spectral extents are specified in a query file.

Other references: 
https://github.com/Open-EO/openeo-community-examples/blob/main/python/10_getting-started/getting-started.ipynb
https://openeo.org/documentation/1.0/cookbook/#scale-all-pixels-linearly-apply-linear-scale-range
"""

import openeo
import os
import yaml


def query_id(query, temporal_id=True):
    spatial_extent = ''
    for k, v in query['spatial_extent'].items():
        spatial_extent += k + '=' + str(v) + '-'
    temporal_extent = query['temporal_extent'][0] + '-' + query['temporal_extent'][1]
    if temporal_id:
        return os.path.join(query['collection'], spatial_extent[:-1], temporal_extent)
    else:
        return os.path.join(query['collection'], spatial_extent[:-1])

if __name__ == "__main__":
    with open('cdse_query.yaml', 'r') as file:
        query = yaml.safe_load(file)

    connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
    connection.authenticate_oidc()

    data_folder = os.path.join(query['data_folder'], query_id(query))

    for band in query['bands']:
        cube = connection.load_collection(
            query['collection'],
            spatial_extent=query['spatial_extent'],
            temporal_extent=query['temporal_extent'],
            bands=[band],
            max_cloud_cover=query['max_cloud_cover']
        )

        job = cube.save_result(
            format="GTiff",
            options={"filename_prefix": f"{query['collection']}_{band}"},
        ).create_job(title=f"S2 {band}")
        job.start_and_wait()
        job.get_results().download_files(os.path.join(data_folder, band))
