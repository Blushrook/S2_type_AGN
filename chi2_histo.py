import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


input_file = 'processed_light_curves_sector03.txt'
output_file = 'reformatted_light_curves_sector03.txt'


def reformat_file(input_filename, output_filename):
    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:

        next(infile)


        for line in infile:
            parts = line.strip().split()
            name = parts[0]
            rest = parts[1:7]
            rest += ['']
            rest += parts[7:]
            outfile.write(f"{name:50s}|{'|'.join(rest)}\n")

    print(f"Reformatted file saved as {output_filename}")


reformat_file(input_file, output_file)


column_names = [
    'Name', 'Objtype', 'Agnclass', 'RA', 'DEC', 'Mean Flux', 'Standard Dev',
    'Weighted Std Dev', 'Sector', 'Camera', 'CCD', 'chi2 Standard',
    'chi2_nu Standard', 'chi2 Normalized', 'chi2_nu Normalized'
]


data = pd.read_csv(output_file, sep='|', names=column_names, header=None)

print("\nFirst few rows of the DataFrame:")
print(data.head())

print("\nData types of the columns:")
print(data.dtypes)


chi2_standard = pd.to_numeric(data['chi2_nu Standard'], errors='coerce')
chi2_normalized = pd.to_numeric(data['chi2_nu Normalized'], errors='coerce')


def print_stats(name, data):
    print(f"\n{name} stats:")
    print(f"Min: {data.min()}, Max: {data.max()}, Mean: {data.mean()}")
    print(f"Number of NaN values: {pd.isna(data).sum()}")
    print(f"Number of infinite values: {np.isinf(data).sum()}")

print_stats("Standard chi2", chi2_standard)
print_stats("Normalized chi2", chi2_normalized)


plt.figure(figsize=(16, 8))


plt.subplot(1, 2, 1)
plt.hist(chi2_standard.dropna(), bins=30, edgecolor='black')
plt.title('Standardized Reduced $\chi^2$')
plt.xlabel('Reduced $\chi^2$')
plt.ylabel('Frequency')


plt.subplot(1, 2, 2)
plt.hist(chi2_normalized.dropna(), bins=30, edgecolor='black')
plt.title('Normalized Reduced $\chi^2$')
plt.xlabel('Reduced $\chi^2$')
plt.ylabel('Frequency')

plt.tight_layout()
plt.savefig('reduced_chi2_histograms_sector03.png', dpi=300, bbox_inches='tight')

print("\nHistogram saved as 'reduced_chi2_histograms_sector03.png'")


os.remove(output_file)
print(f"Temporary file {output_file} removed.")
~                                                  
