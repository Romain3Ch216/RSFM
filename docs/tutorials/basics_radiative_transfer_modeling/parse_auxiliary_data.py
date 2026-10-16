import os
import glob
import json
import argparse
import xarray as xr

from eodal_s2_parsing import parse_MTD_TL, parse_MTD_MSI


def open_grib(path):
    # several parameter types can share a file, so open per shortName if needed
    return xr.open_dataset(path, engine="cfgrib",
                           backend_kwargs={"indexpath": ""})


def get_atmosphere_data(L1C_folder: str, lat: float, lon: float):
    """Parse atmospheric data from AUX_ECMWFT and convert variables for py6s.
    """
    ds = open_grib(glob.glob(os.path.join(L1C_folder, 'GRANULE/*/AUX_DATA/AUX_ECMWFT'))[0])
    pt = ds.sel(latitude=lat, longitude=lon % 360, method="nearest") 

    tcwv = float(pt["tcwv"])   # kg/m2  (~ mm)
    tco3 = float(pt["tco3"])   # kg/m2
    msl  = float(pt["msl"])    # Pa

    # unit conversions for 6S
    water_g_cm2 = tcwv / 10.0               # kg/m2 -> g/cm2
    ozone_cm_atm = tco3 / 2.1415e-5 / 1000  # kg/m2 -> DU -> atm-cm


    cams = open_grib(glob.glob(os.path.join(L1C_folder, 'GRANULE/*/AUX_DATA/AUX_CAMSFO'))[0])
    c = cams.sel(latitude=lat, longitude=lon % 360, method="nearest")
    aot550 = float(c["aod550"])

    return {
        'TOTAL_COLUMN_WATER_VAPOR': {'VALUE': water_g_cm2, 'UNIT': 'g/cm2'},
        'TOTAL_COLUMN_OZONE': {'VALUE': ozone_cm_atm, 'UNIT': 'Dobson Unit'},
        'PRESSURE_AT_MEAN_SEA_LEVEL': {'VALUE': msl, 'UNIT': 'Pa'},
        'AOT_550': {'VALUE': aot550, 'UNIT': None},
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--L1C_folder', type=str, help='Path to the L1C data.')
    parser = parser.parse_args()

    L1C_folder = parser.L1C_folder
    aux_geometry_data = parse_MTD_TL(glob.glob(os.path.join(L1C_folder, 'GRANULE/*/MTD_TL.xml'))[0])
    aux_atmosphere_data = get_atmosphere_data(
        L1C_folder,
        lat=aux_geometry_data['ULX'],
        lon=aux_geometry_data['ULY'])
    
    aux_data = {
        'AUX_GEOMETRY_DATA': aux_geometry_data,
        'AUX_ATMOSPHERIC_DATA': aux_atmosphere_data,
    }

    out_folder = glob.glob(os.path.join(L1C_folder, 'GRANULE/*/'))[0]

    with open(os.path.join(out_folder, 'auxiliary_data.json'), 'w') as f:
        json.dump(aux_data, f, indent=4)

    metadata = parse_MTD_MSI(os.path.join(L1C_folder, 'MTD_MSIL1C.xml'))

    with open(os.path.join(L1C_folder, 'MTD_MSIL1C.json'), 'w') as f:
        json.dump(metadata, f, indent=4)