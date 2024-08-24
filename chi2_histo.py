import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import glob
import os
import pandas as pd

def process_file(file_path):
    try:
        with open(file_path, 'r') as f:
            header = f.readline().strip()
        columns = header.split()
        data = pd.read_csv(file_path, delim_whitespace=True, names=columns, skiprows=1)

    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return None, None

    print(f"\nColumns in {file_path}:")
    print(data.columns.tolist())

    if 'Chi2_reduced_Normalized' not in data.columns or 'Chi2_reduced_Standardized' not in data.columns:
        print(f"Error: Required columns not found in {file_path}")
        return None, None

    normalized_chi2 = data['Chi2_reduced_Normalized'].values
    standardized_chi2 = data['Chi2_reduced_Standardized'].values

    return normalized_chi2, standardized_chi2

def plot_histogram_with_pdf(chi2_values, title, output_path):
    if chi2_values is None or len(chi2_values) == 0:
        print(f"Warning: No data to plot for {title}")
        return
    chi2_values = np.array(chi2_values)
    plt.figure(figsize=(15, 6))
    plt.subplot(121)
    positive_chi2 = chi2_values[chi2_values > 0]

    if len(positive_chi2) > 0:
        n, bins, _ = plt.hist(positive_chi2, bins=30, density=True, alpha=0.7, edgecolor='black')
        adjusted_chi2 = positive_chi2 * 1000
        x = np.linspace(min(adjusted_chi2)max(adjusted_chi2), 100)
        df = len(positive_chi2)
        chi2_pdf = stats.chi2.pdf(x, df)

        plt.plot(x, chi2_pdf / 1000, 'r-', lw=2, label=f'Chi2 PDF (df={df: .2f})')

        plt.title(f'{title} - Full Distribution')
        plt.xlabel('Reduced Chi2')
        plt.ylabel('Density')
        plt.legend()
    else:
        plt.text(0.5, 0.5, "No positive values to plot", ha='center', va='center')

    plt.subplot(122)
    top_50 = np.sort(chi2_values)[-50:]
    plt.hist(top_50, bins=10, edgecolor='black')
    plt.title(f'{title} - Top 50 Values')
    plt.xlabel('Reduced Chi2')
    plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Plot saved: {output_path}")

def main():
    txt_files = glob.glob('*.txt')
    total_files = len(txt_files)
    valid_files = 0

    all_normalized_chi2 = np.array([])
    all_standardized_chi2 = np.array([])

    for file_path in txt_files:
        normalized_chi2, standardized_chi2 = process_file(file_path)

        if normalized_chi2 is not None and standardized_chi2 is not None:
            valid_files += 1

            print(f"\nFile: {file_path}")
            print(f"Normalized Chi2: {len(normalized_chi2)} values, {np.sum(normalized_chi2 > 0)} positive")
            print(f"Standardized Chi2: {len(standardized_chi2)} values, {np.sum(standardized_chi2 > 0)} positive")

            all_normalized_chi2 = np.concatenate([all_normalized_chi2, normalized_chi2])
            all_standardized_chi2 = np.concatenate([all_standardized_chi2, standardized_chi2])

            output_dir = f'output_{os.path.splitext(file_path)[0]}'
            os.makedirs(output_dir, exist_ok=True)

            plot_histogram_with_pdf(normalized_chi2, f'Normalized Chi2 - {os.path.basename(file_path)}',
                                    f'{output_dir}/normalized_chi2_histogram.png')
            plot_histogram_with_pdf(standardized_chi2, f'Standardized Chi2 - {os.path.basename(file_path)}',
                                    f'{output_dir}/standardized_chi2_histogram.png')
        else:
            print(f"\nSkipping {file_path} due to errors.")

    if valid_files > 0:
        os.makedirs('combined_output', exist_ok=True)
        plot_histogram_with_pdf(all_normalized_chi2, 'Combined Normalized Chi2',
                                'combined_output/combined_normalized_chi2_histogram.png')
        plot_histogram_with_pdf(all_standardized_chi2, 'Combined Standardized Chi2',
                                'combined_output/combined_standardized_chi2_histogram.png')

    print(f"\nProcessing complete.")
    print(f"Total files processed: {total_files}")
    print(f"Files with valid data: {valid_files}")
    print("Check the output directories for results.")

if __name__ == "__main__":
    main()
