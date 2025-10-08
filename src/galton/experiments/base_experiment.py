from abc import ABC, abstractmethod
from pathlib import Path
import matplotlib.pyplot as plt


class BaseExperiment(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def run(self):
        """Run the experiment and store results in attributes."""
        pass

    @abstractmethod
    def plot(self, save_folder=None):
        """Generate and save a plot."""
        pass

    def save_plot(self, fig, save_folder, filename=None):
        folder = Path(save_folder)
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / f"{filename or self.name}.png"
        fig.savefig(file_path)
        print(f"[✓] Saved plot to {file_path}")
        plt.close(fig)
