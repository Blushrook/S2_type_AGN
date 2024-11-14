import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import glob
from matplotlib.projections.geo import GeoAxes
import pandas as pd

agn_catalogs = [
    'eFEDS_c001_hard_V6.2.fits.gz',
    'eFEDS_c001_main_V6.2.fits.gz',
    'etaCha_c001_hard_V1.fits.gz',
    'etaCha_c001_main_V1.fits.gz'
]

ra_list = []
dec_list = []

for catalog in agn_catalogs:
    with fits.open(catalog) as hdul:
        data = hdul[1].data
        ra_list.extend(data['RA'])
        dec_list.extend(data['DEC'])

ra_agn = np.array(ra_list)
dec_agn = np.array(dec_list)

objects = pd.read_csv('List.txt', header=None)[0].tolist()

columns = ['Name', 'Objtype', 'Agnclass', 'RA', 'DEC', 'Mean_Flux', 'Stddev', 'Sector', 'Camera', 'CCD', 'Chi2_Normalized', 'Chi2_reduced_Normalized','Chi2_Standardized', 'Chi2_reduced_Standardized']

light_curves = glob.glob('processed_light_curves*.txt')
matched_ra = []
matched_dec = []

for curve_file in light_curves:
    df = pd.read_csv(curve_file, delim_whitespace=True, names=columns)
    matched_objects = df[df['Name'].isin(objects)]
    matched_ra.extend(matched_objects['RA'].tolist())
    matched_dec.extend(matched_objects['DEC'].tolist())

matched_ra = np.array(matched_ra, dtype=float)
matched_dec = np.array(matched_dec, dtype=float)

l = np.zeros(len(ra_agn))
b = np.zeros(len(ra_agn))

for i in range(len(ra_agn)):
    b[i] = dec_agn[i] * np.pi/180
    if ra_agn[i] < 180:
        l[i] = -(ra_agn[i] * np.pi/180)
    else:
        l[i] = 2*np.pi - (ra_agn[i] * np.pi/180)

l_tess = np.zeros(len(matched_ra))
b_tess = np.zeros(len(matched_ra))

for i in range(len(matched_ra)):
    b_tess[i] = matched_dec[i] * np.pi/180.0
    if matched_ra[i] < 180:
        l_tess[i] = -(matched_ra[i] * np.pi/180.0)
    else:
        l_tess[i] = 2*np.pi - (matched_ra[i] * np.pi/180.0)

fig = plt.figure(figsize=(16, 10))
ax = plt.subplot(111, projection='mollweide')
ax.scatter(l, b, color='red', s=20, alpha=0.6, label='eRosita')
ax.scatter(l_tess, b_tess, color='green', s=20, alpha=0.6, label='TESS')
plt.grid(True)

plt.legend(fontsize=15)
plt.title('TESS vs eRosita', fontsize=20)
plt.tight_layout(pad=0.9)

plt.savefig('agn_map_mollweide.png', dpi=300, bbox_inches='tight')
plt.close()
