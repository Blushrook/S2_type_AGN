import glob
import pandas as pd
from pathlib import Path
import requests
from astropy_healpix import HEALPix
from astropy.coordinates import SkyCoord

def get_erosita_data(ra, dec):
    hpix = HEALPix(nside=2**16, order='nested', frame='icrs')
    coord = SkyCoord(ra, dec, unit='deg')
    hpidx = hpix.skycoord_to_healpix(coord)
    
    band = '024'
    url = f'https://sciserver.mpe.mpg.de/erosita-ul/ULbyHP/{band}/{hpidx}'
    
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('flux'), data.get('flux_err')
    except:
        return None, None

with open('interesting.txt', 'r') as f:
    interesting_objects = set(f.read().splitlines()
                              
object_info = {}
all_files = glob.glob('processed_light_curves_sector*.txt')

for file in all_files:
    df = pd.read_csv(file, delim_whitespace=True)
    mask = df['Name'].isin(interesting_objects)
    filtered_df = df[mask]
    
    for _, row in filtered_df.iterrows():
        if row['Name'] not in object_info:
            object_info[row['Name']] = {
                'RA': row['RA'],
                'DEC': row['DEC'],
                'Agnclass': row['Agnclass'],
                'Sector': row['Sector'],
                'Camera': row['Camera']
            }

results = []
for name, info in object_info.items():
    erosita_flux, flux_error = get_erosita_data(info['RA'], info['DEC'])
    
    results.append({
        'Name': name,
        'Agnclass': info['Agnclass'],
        'RA': info['RA'],
        'DEC': info['DEC'],
        'Sector': info['Sector'],
        'Camera': info['Camera'],
        'eROSITA_Flux': erosita_flux,
        'Flux_Error': flux_error
    })

result_df = pd.DataFrame(results)
result_df.to_csv('AGN_interesting_objects.txt', index=False, sep='\t')

print("Results saved to AGN_interesting_objects.txt")
print(result_df)
