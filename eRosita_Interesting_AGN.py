import glob
import pandas as pd
from pathlib import Path
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

def get_erosita_data(ra, dec, catalog_files):
    best_match_flux = None
    best_match_flux_err = None
    best_sep = float('inf')
    found = False

    print(f"\nSearching for object at RA={ra}, DEC={dec}")

    for catalog_path in catalog_files:
        with fits.open(catalog_path) as hdul:
            catalog_data = hdul[1].data
            print(f"\nProcessing catalog: {catalog_path}")
            print(f"Number of souces in catalog: {len(catalog_data)}")

            catalog_coords = SkyCoord(catalog_data['RA'], catalog_data['DEC'],
                                    unit=(u.degree, u.degree))
            target_coord = SkyCoord(ra, dec, unit=u.degree)

            idx, sep, _ = target_coord.match_to_catalog_sky(catalog_coords)
            print(f"closest match separation: {sep.arcsec[0]: .2f} arcsec")

            if sep.arcsec[0] < 30 and sep.arcsec[0] < best_sep:
                found = True
                best_sep = sep.arcsec[0]
                best_match_flux = float(catalog_data['ML_FLUX'][idx])
                best_match_flux_err = float(catalog_data['ML_FLUX_ERR'][idx])
                print(f"Match found in {catalog_path}")
                print(f"Separation: {best_sep:.2f} arcsec")
                print(f"Flux: {best_match_flux:.6e}")
                print(f"Flux Error: {best_match_flux_err:.6e}")

    if found:
        print("Object found.")
    if not found:
        print("No match found in any catalog within 30 arcsec!")

    return best_match_flux, best_match_flux_err


print("Reading List.txt")
with open('List.txt', 'r') as f:
    interesting_objects = set(f.read().splitlines())
print(f"Found {len(interesting_objects)} objects in List.txt")


object_info = {}
processed_coords = set()

all_files = glob.glob('processed_light_curves_sector*.txt')
print(f"\nProcessing {len(all_files)} light curve files")

for file in all_files:
    print(f"Reading {file}")
    df = pd.read_csv(file, delim_whitespace=True)
    mask = df['Name'].isin(interesting_objects)
    filtered_df = df[mask]

    for _, row in filtered_df.iterrows():
        coord_key = f"{row['RA']:.6f}_{row['DEC']:.6f}"

        if coord_key not in processed_coords:
            processed_coords.add(coord_key)
            object_info[row['Name']] = {
                'RA': row['RA'],
                'DEC': row['DEC'],
                'Agnclass': row['Agnclass'],
                'Sector': row['Sector'],
                'Camera': row['Camera'],
                'CCD': row['CCD']
            }

print(f"\nFound {len(object_info)} unique objects")


catalog_files = ['etaCha_c001_main_V1.fits.gz']


results = []
print("\nMatching objects with eROSITA catalogs")
for name, info in object_info.items():
    print(f"\nProcessing object: {name}")
    erosita_flux, flux_error = get_erosita_data(info['RA'], info['DEC'], catalog_files)

    result_dict = {
        'Name': name,
        'Agnclass': info['Agnclass'],
        'RA': info['RA'],
        'DEC': info['DEC'],
        'Sector': info['Sector'],
        'Camera': info['Camera'],
        'CCD': info['CCD'],
        'eROSITA_Flux': erosita_flux,
        'Flux_Error': flux_error
    }

    print("Result dictionary:")
    for key, value in result_dict.items():
        print(f"{key}: {value}")

    results.append(result_dict)


result_df = pd.DataFrame(results)
output_file = 'AGN_interesting_objects.txt'

result_df.to_csv(output_file,
                 index=False,
                 sep='\t',
                 float_format='%.6e',
                 na_rep='NaN')

print(f"\nResults saved to {output_file}")
print("\nFinal DataFrame:")
print(result_df)
~                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 ~               
