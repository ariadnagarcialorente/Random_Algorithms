from random import randrange
import numpy as np
import matplotlib.pyplot as plt

from .base_experiment import BaseExperiment


class GaltonTriangleMatrix(BaseExperiment):
    def __init__(self, height, balls):
        super().__init__("galton_board")
        self.height = height
        self.balls = balls
        self.board = None

    def run(self):
        board = np.zeros((self.height, self.height), dtype=int)
        for _ in range(self.balls):
            i, j = 0, 0
            for _ in range(self.height - 1):
                if randrange(2) == 0:
                    i += 1
                else:
                    j += 1
            board[i][j] += 1
        self.board = board
        print(f"[✓] Simulation complete ({self.balls} balls, height={self.height})")

    def plot(self, save_folder=None, filename=None):
        if self.board is None:
            raise RuntimeError("Run the experiment before plotting.")
        fig, ax = plt.subplots(figsize=(6, 6))
        im = ax.imshow(self.board, cmap="hot", origin="upper")
        fig.colorbar(im, ax=ax, label="Number of balls")
        ax.set_title(f"Galton Board: Final Positions of Balls \n (height={self.height}, balls={self.balls})")
        ax.set_xlabel("Row (i)")
        ax.set_ylabel("Column (j)")
        # Use dynamic folder if provided

        if save_folder:
            self.save_plot(fig, save_folder=save_folder, filename=filename)
        else:
            plt.show()