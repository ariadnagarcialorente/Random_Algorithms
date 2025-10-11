import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
from itertools import product
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

from .base_experiment import BaseExperiment


class GaltonBinomial(BaseExperiment):
    def __init__(self, heights: list[int], balls_list: list[int]):
        super().__init__("galton_binomial")
        self.heights = heights
        self.balls_list = balls_list
        self.results = {}  # {(height, balls): (simulated_probs, theoretical_probs, mse)}

    def run(self):
        """
        Run Galton simulations for all (height, balls) combinations.
        Compute theoretical binomial PMF and store MSE between them.
        """
        for h, b in product(self.heights, self.balls_list):
            results = np.random.binomial(h, 0.5, size=b)
            counts, _ = np.histogram(results, bins=np.arange(h + 2), density=True)
            x = np.arange(h + 1)
            pmf = binom.pmf(x, h, 0.5)

            mse = np.mean((counts - pmf) ** 2)
            self.results[(h, b)] = (x, counts, pmf, mse)

    def plot(self, save_folder=None, filename=None, use_3d=False):
        if not self.results:
            raise RuntimeError("You must call `run()` before plotting.")

        # --- 1. Individual comparisons ---
        for (h, b), (x, counts, pmf, mse) in self.results.items():
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(x, counts, width=0.8, alpha=0.6, label=f"Galton simulation (balls={b})")
            ax.plot(x, pmf, "r--", lw=2, label="Binomial PMF (theoretical)")
            ax.set_title(f"Galton vs Binomial (height={h}, balls={b})\nMSE={mse:.4e}")
            ax.set_xlabel("Final ball position")
            ax.set_ylabel("Probability")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.5)

            if save_folder:
                self.save_plot(fig, save_folder, f"{filename or self.name}_h{h}_b{b}.png")
            else:
                plt.show()

        # --- 2. MSE trend heatmap ---
        heights_arr = np.array([h for (h, _) in self.results.keys()])
        balls_arr = np.array([b for (_, b) in self.results.keys()])
        mse_arr = np.array([mse for (_, _, _, mse) in self.results.values()])

        fig, ax = plt.subplots(figsize=(7, 5))
        sc = ax.tricontourf(heights_arr, balls_arr, mse_arr, cmap="viridis")
        plt.colorbar(sc, ax=ax, label="Mean Squared Error")
        ax.set_xlabel("Height")
        ax.set_ylabel("Number of Balls")
        ax.set_title("MSE between Galton Simulation and Binomial PMF")

        if save_folder:
            self.save_plot(fig, save_folder, f"{filename or self.name}_mse_heatmap.png")
        else:
            plt.show()

        # --- 3. Optional 3D surface plot ---
        if use_3d:
            fig = plt.figure(figsize=(8, 6))
            ax = fig.add_subplot(projection="3d")
            ax.plot_trisurf(heights_arr, balls_arr, mse_arr, cmap=cm.viridis, edgecolor="none")
            ax.set_xlabel("Height")
            ax.set_ylabel("Number of Balls")
            ax.set_zlabel("MSE")
            ax.set_title("3D Error Surface: Galton vs Binomial")

            if save_folder:
                self.save_plot(fig, save_folder, f"{filename or self.name}_mse_surface.png")
            else:
                plt.show()

        return fig
