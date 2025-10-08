from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom, norm

from .base_experiment import BaseExperiment


class BinomialNormal(BaseExperiment):
    def __init__(self, n_values=None, N=10000):
        """
        Compare the Binomial(n, 1/2) distribution to its Normal approximation N(n/2, n/4).

        Args:
            n_values (list[int]): List of n values to test. Default [10, 50, 100, 500, 1000].
            N (int): Number of random samples drawn from Binomial(n, 1/2).
        """
        super().__init__("binomial_normal")
        self.n_values = n_values or [10, 50, 100, 500, 1000]
        self.N = N
        self.results = {}

    def run(self):
        for n in self.n_values:
            p = 0.5
            mu = n * p
            sigma2 = n * p * (1 - p)
            sigma = np.sqrt(sigma2)

            # Empirical samples
            samples = np.random.binomial(n, p, self.N)
            values, counts = np.unique(samples, return_counts=True)
            empirical_pmf = counts / self.N

            # Theoretical Binomial PMF
            binomial_pmf = binom.pmf(values, n, p)

            # Normal approximation (evaluated at integer k values)
            normal_pdf = norm.pdf(values, loc=mu, scale=sigma)
            normal_pdf /= normal_pdf.sum()  # Normalize to approximate PMF

            # Mean squared error between binomial PMF and normal PDF
            mse = np.mean((binomial_pmf - normal_pdf) ** 2)

            self.results[n] = {
                "values": values,
                "empirical_pmf": empirical_pmf,
                "binomial_pmf": binomial_pmf,
                "normal_pdf": normal_pdf,
                "mse": mse,
            }

    def plot(self, save_folder=None, filename=None):
        if not self.results:
            raise RuntimeError("You must call .run() before .plot()")

        if save_folder:
            save_folder = Path(save_folder)
            save_folder.mkdir(parents=True, exist_ok=True)

        # Plot distributions for each n
        for n, data in self.results.items():
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.bar(
                data["values"],
                data["binomial_pmf"],
                width=0.8,
                color="skyblue",
                label=f"Binomial(n={n}, p=0.5)"
            )
            ax.plot(
                data["values"],
                data["normal_pdf"],
                "k-",
                label=f"Normal($\\mu$={n / 2}, $\\sigma^2$={n / 4:.1f})"
            )
            ax.set_title(f"Binomial vs Normal (n={n})")
            ax.set_xlabel("k")
            ax.set_ylabel("Probability")
            ax.legend()
            ax.grid(True, linestyle="--", alpha=0.4)
            fig.tight_layout()

            if save_folder:
                fig.savefig(save_folder / f"{filename or 'binomial_vs_normal'}_n{n}.png")
                plt.close(fig)
            else:
                plt.show()

        # Plot MSE vs n
        fig, ax = plt.subplots(figsize=(6, 4))
        n_values = list(self.results.keys())
        mse_values = [self.results[n]["mse"] for n in n_values]
        ax.plot(n_values, mse_values, "o-", color="darkred")
        ax.set_title("Mean Squared Error: Binomial vs Normal Approximation")
        ax.set_xlabel("n")
        ax.set_ylabel("MSE")
        ax.grid(True, alpha=0.4)
        fig.tight_layout()

        if save_folder:
            fig.savefig(save_folder / f"{filename or 'mse_vs_n'}.png")
            plt.close(fig)
        else:
            plt.show()
