"""

| Parameter   | Description of parameter        | Units        |Typical min | Typical max |
|-------------|---------------------------------|--------------|------------|-------------|
|   N         | Leaf structure parameter        | N/A          | 0.8        | 2.5         |
|  cab        | Chlorophyll a+b concentration   | ug/cm2       | 0          | 80          |
|  caw        | Equivalent water thickiness     | cm           | 0          | 200         |
|  car        | Carotenoid concentration        | ug/cm2       | 0          | 20          |
|  cbrown     | Brown pigment                   | NA           | 0          | 1           |
|  cm         | Dry matter content              | g/cm2        | 0          | 200         |
|  lai        | Leaf Area Index                 | N/A          | 0          | 10          |
|  lidfa      | Leaf angle distribution         | N/A          | -          | -           |
|  lidfb      | Leaf angle distribution         | N/A          | -          | -           |
|  psoil      | Dry/Wet soil factor             | N/A          | 0          | 1           |
|  rsoil      | Soil brigthness factor          | N/A          | -          | -           |
|  hspot      | Hotspot parameter               | N/A          | -          | -           |
|  tts        | Solar zenith angle              | deg          | 0          | 90          |
|  tto        | Observer zenith angle           | deg          | 0          | 90          |
|  phi        | Relative azimuth angle          | deg          | 0          | 360         |
"""
import prosail
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pdb

n = 10
cab = 40
car = 8
cbrown = 0
cw = 0.01
cm = 0


LEAF_TRAITS = {
    'N': {'desc': 'Leaf structure parameter', 'range': [1.0, 2.5], 'default': 1.5, 'unit': None},
    'Cab': {'desc': 'Chlorophyll a+b concentration', 'range': [20, 80], 'default': 40, 'unit': 'µg/cm²'},
    'Car': {'desc': 'Cartenoid concentration', 'range': [3, 15], 'default': 8, 'unit': 'µg/cm²'},
    'Cbrown': {'desc': 'Brown pigment', 'range': [0, 1], 'default': 0, 'unit': None},
    'Cw': {'desc': 'Equivalent water thickness', 'range': [0.005, 0.04], 'default': 0.015, 'unit': 'cm'},
    'Cm': {'desc': 'Dry matter', 'range': [0.002, 0.02], 'default': 0.009, 'unit': 'g/cm²'}
}

n_values = 8
fontsize = 15

colors = sns.color_palette("crest", n_values)
traits = dict((k, v['default']) for k, v in LEAF_TRAITS.items())

for trait in LEAF_TRAITS:
    range_trait = LEAF_TRAITS[trait]['range']
    trait_values = np.linspace(range_trait[0], range_trait[1], n_values)
    fig, ax = plt.subplots()
    for i, trait_value in enumerate(trait_values):
        traits[trait] = trait_value
        lam, rho, tau = prosail.run_prospect(traits['N'], traits['Cab'], traits['Car'], traits['Cbrown'], traits['Cw'], traits['Cm'])
        unit = LEAF_TRAITS[trait]['unit'] if LEAF_TRAITS[trait]['unit'] is not None else ''
        label = f'{trait}={trait_value:.2f}{unit}' if i % 2 == 0 else None
        plt.plot(lam, rho, color=colors[i], label=label)
    plt.xlabel(f'Wavelength (µm)', fontsize=fontsize)
    plt.ylabel('Reflectance', fontsize=fontsize)
    plt.legend(fontsize=int(0.75*fontsize))
    plt.grid()
    plt.show()