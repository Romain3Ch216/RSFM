"""
Usage: python simulate_radiance_from_reflectance.py --L1C_folder ../data/S2B_MSIL1C_20261005T102859_N0513_R108_T31UGP_20261005T140445.SAFE/
"""

import os
import json
import glob
import argparse
import numpy as np
from datetime import datetime
from typing import List, Dict

import Py6S as pyrtm


SENTINEL2_WV = [
    0.4423,
    0.4923,
    0.5590,
    0.6649,
    0.7038,
    0.7391,
    0.7797,
    0.8329,
    0.8640,
    0.9432,
    1.3769,
    1.6104,
    2.1857
    ]


def radiative_transfer_modeling_6S(aux_data: Dict, wavelengths: List):
    geometry_data = aux_data['AUX_GEOMETRY_DATA']
    atmosphere_data = aux_data['AUX_ATMOSPHERIC_DATA']

    E_TOA, E_dir, E_dif, E_env, T_down, T_up, T_gas, S_alb, L_path, xa, xb, xc = \
        [], [], [], [], [], [], [], [], [], [], [], []
    for i in range(len(wavelengths)):
        s = pyrtm.SixS()
        
        s.geometry = pyrtm.Geometry.User()
        s.geometry.solar_z, s.geometry.solar_a = geometry_data['SUN_ZENITH_ANGLE'], geometry_data['SUN_AZIMUTH_ANGLE']
        s.geometry.view_z,  s.geometry.view_a  = geometry_data['SENSOR_ZENITH_ANGLE'], geometry_data['SENSOR_AZIMUTH_ANGLE']
        acquisition_date = datetime.strptime(
            geometry_data['SENSING_TIME'].split("T")[0], "%Y-%m-%d"
        ).date()
        s.geometry.month, s.geometry.day = acquisition_date.month, acquisition_date.day

        s.atmos_profile = pyrtm.AtmosProfile.UserWaterAndOzone(
            atmosphere_data['TOTAL_COLUMN_WATER_VAPOR']['VALUE'], 
            atmosphere_data['TOTAL_COLUMN_OZONE']['VALUE']
            )
        s.aero_profile  = pyrtm.AeroProfile.Continental
        s.aot550 = atmosphere_data['AOT_550']['VALUE']

        s.altitudes.set_sensor_satellite_level()
        s.altitudes.set_target_pressure(atmosphere_data['PRESSURE_AT_MEAN_SEA_LEVEL']['VALUE'])

        # s.ground_reflectance = pyrtm.GroundReflectance.HomogeneousLambertian(0.3)
        # s.atmos_corr = pyrtm.AtmosCorr.AtmosCorrLambertianFromReflectance(0.3)  # gives xa, xb, xc
        s.wavelength = pyrtm.Wavelength(wavelengths[i])
        s.run()
        o = s.outputs

        E_TOA.append(o.solar_spectrum)
        E_dir.append(o.direct_solar_irradiance)
        E_dif.append(o.diffuse_solar_irradiance)
        E_env.append(o.environmental_irradiance)
        T_down.append(o.transmittance_total_scattering.downward)
        T_up.append(o.transmittance_total_scattering.upward)
        T_gas.append(o.transmittance_global_gas.total)
        S_alb.append(o.spherical_albedo.total)
        L_path.append(o.atmospheric_intrinsic_radiance)
        xa.append(o.coef_xa)
        xb.append(o.coef_xb)
        xc.append(o.coef_xc)

    output = {
        'DIRECT_SOLAR_IRRADIANCE': {'VALUES': E_dir, 'UNIT': 'W/m2/µm'},
        'DIFFUSE_SOLAR_IRRADIANCE': {'VALUES': E_dif, 'UNIT': 'W/m2/µm'},
        'ENVIRONMENTAL_SOLAR_IRRADIANCE': {'VALUES': E_env, 'UNIT': 'W/m2/µm'},
        'TRANSMITTANCE_TOTAL_SCATTERING_DOWNWARD': {'VALUES': T_down, 'UNIT': None},
        'TRANSMITTANCE_TOTAL_SCATTERING_UPWARD': {'VALUES': T_up, 'UNIT': None},
        'TRANSMITTANCE_TOTAL_GAS': {'VALUES': T_gas, 'UNIT': None},
        'SPHERICAL_ALBEDO': {'VALUES': S_alb, 'UNIT': None},
        'ATMOSPHERIC_INTRINSIC_RADIANCE': {'VALUES': L_path, 'UNIT': 'W/m2/sr/µm'},
        'SOLAR_SPECTRUM': {'VALUES': E_TOA, 'UNIT': 'W/m2/sr/µm'},
        'WAVELENGTHS': {'VALUES': list(wavelengths), 'UNIT': 'µm'}
    }

    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--L1C_folder', type=str, help='Path to the L1C data.')
    parser.add_argument('--wv', type=str, help='S2 or HYP')
    parser = parser.parse_args()

    L1C_folder = parser.L1C_folder
    in_folder = glob.glob(os.path.join(L1C_folder, 'GRANULE/*/'))[0]

    if parser.wv == 'S2':
        wv = SENTINEL2_WV
        file_path = os.path.join(in_folder, 'radiative_variables.json')
    elif parser.wv == 'HYP':
        wv = np.linspace(0.4, 2.5, 300)
        file_path = './data/radiative_variables.json'
    else:
        raise ValueError("wv must be in ['S2', 'HYP']")

    with open(os.path.join(in_folder, 'auxiliary_data.json'), 'r') as f:
        aux_data = json.load(f)

    if os.path.exists(file_path):
        print('File aready exists.')
    else:
        radiative_variables = radiative_transfer_modeling_6S(aux_data, wv)

        # Handle NaN values
        for var_name, var in radiative_variables.items():
            var = np.array(var['VALUES'])
            mask = np.isnan(var)
            var[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), var[~mask])
            radiative_variables[var_name]['VALUES'] = [float(x) for x in var]

        with open(file_path, 'w') as f:
            json.dump(radiative_variables, f, indent=4)