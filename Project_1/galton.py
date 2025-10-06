from random import randrange
import numpy as np
import matplotlib.pyplot as plt
import argparse

def galton_board(h, b):
    board = np.zeros((h, h), dtype=int)
    for _ in range(b):
        i, j = 0, 0
        for step in range(h-1):  # move h-1 times to stay inside board
            if randrange(2) == 0:
                i += 1
            else:
                j += 1
        board[i][j] += 1  # mark final position only
    return board

def print_graph(dataset):
    plt.figure(figsize=(6,6))
    plt.imshow(dataset, cmap='hot', origin='upper')
    plt.colorbar(label='Number of balls')
    plt.title('Galton Board: Final Positions of Balls')
    plt.xlabel('Column (j)')
    plt.ylabel('Row (i)')
    plt.show()

# Parse arguments
parser = argparse.ArgumentParser(description="Generate a Galton board simulator.")
parser.add_argument("--height", "-H", type=int, required=True, help="number of choices each ball makes")
parser.add_argument("--balls", "-B", type=int, required=True, help="number of balls dropped")
args = parser.parse_args()

board = galton_board(args.height, args.balls)
print_graph(board)
