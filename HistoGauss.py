import numpy as np
import matplotlib.pyplot as plt
import os
import logging
from scipy import stats
from LightCurve2 import LightCurveData

class HistoGaussData:
    def __init__(self, directory, save_directory, light_curve_data):
        self.directory = directory
        self.save_directory = save_directory
        os.makedirs(self.save_directory, exist_ok=True)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.light_curve_data = light_curve_data

    def plot_histogram(self, data, title, filename, num_bins=30):
        data = data[np.isfinite(data)]
        if len(data) == 0:
            logging.warning(f"No finite data points for {title}")
            return None, None, None, None

        plt.figure(figsize=(10, 6))
        n, bins, _ = plt.hist(data, bins=num_bins, density=True, alpha=0.7)

        mu, sigma = stats.norm.fit(data)
        x = np.linspace(np.min(data), np.max(data), 100)
        gaussian = stats.norm.pdf(x, mu, sigma)
        plt.plot(x, gaussian, 'r-', lw=2, label='Gaussian fit')

        plt.title(title)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig(os.path.join(self.save_directory, filename))
        plt.close()

        return n, bins, mu, sigma

    def calculate_chi2(self, clipped_data):
        chi2 = stats.chi2(clipped_data)
        dof = len(clipped_data) - 1
        reduced_chi2 = chi2 / dof
        return chi2, reduced_chi2

    def calculate_and_plot_histograms(self, filename, obj_name, num_bins=100):
        test1_data = (clipped_data['cts'] - stddev) / n_points
        non_finite = np.sum(~np.isfinite(test1_data))
        if non_finite > 0:
            logging.warning(f"{obj_name}: Test 1 data contains {non_finite} non-finite values")
            test1_data = test1_data[~np.isfinite(test1_data)]
        n1, bins1, mu1, sigma1 = self.plot_histogram(
            test1_data,
            f"Test 1 Histogram for {obj_name}",
            f"{obj_name}_test1_histogram.png",
            num_bins
         )

        chi2_1, reduced_chi2_1 = self.calculate_chi2(
            test1_data,
            np.zeros_like(test1_data),
            np.ones_like(test1_data)
        )


        test2_data = clipped_data['cts'] / clipped_data['e_cts']
        non_finite = np.sum(~np.isfinite(test2_data))
        if non_finite > 0:
            logging.warning(f"{obj_name}: Test 2 data contains {non_finite} non-finite values")
            test2_data = test2_data[np.isfinite(test2_data)]

          n2, bins2, mu2, sigma2 = self.plot_histogram(
            test2_data,
            f"Test 2 Histogram for {obj_name}",
            f"{obj_name}_test2_histogram.png",
            num_bins
        )

        chi2_2, reduced_chi2_2 = self.calculate_chi2(
            test2_data,
            np.zeros_like(test2_data),
            np.ones_like(test2_data)
        )

        return (chi2_1, reduced_chi2_1), (chi2_2, reduced_chi2_2), mean_flux, stddev
            else:
                logging.warning(f"No data after sigma clipping for {obj_name}")
        else:
            logging.warning(f"Required columns not found in data for {obj_name}")
        return None, None, None, None
~                                         
