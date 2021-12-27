import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button
import numpy as np


def plot_piece(piece):
    axes = [3, 3, 3]

    data = np.zeros(axes, dtype=bool)
    for x, y, z in piece:
        data[x, y, z] = 1

    alpha = 0.9
    
    colors = np.empty(axes + [4], dtype=np.float32)
    
    colors[:] = [1, 0, 0, alpha]  # red

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.voxels(data, facecolors=colors, edgecolors='black')
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_zticks([0, 1, 2])
    plt.show()

def plot_pieces(pieces):
    axes = [3, 3, 3]

    data = np.zeros(axes, dtype=bool)
    alpha = 0.5
    
    colors = np.empty(axes + [4], dtype=np.float32)
    edge_colors = np.empty(axes + [4], dtype=np.float32)
    
    colors[:] = [0.7, 0.7, 0.7, 0.4]  # light gray background
    edge_colors[:] = [0, 0, 0, 0]  # none

    for p, piece in enumerate(pieces):
        for x, y, z in piece:
            data[x, y, z] = 1
            
            if p == len(pieces) - 1:
                # highlight last piece
                colors[x, y, z, :] = [1, 0, 0, 0.9]
                edge_colors[x, y, z, :] = [0, 0, 0, 1]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.voxels(data, facecolors=colors, edgecolors=edge_colors)
    ax.set_xticks([0, 1, 2])
    ax.set_yticks([0, 1, 2])
    ax.set_zticks([0, 1, 2])
    plt.show()

if __name__ == "__main__":
    import pieces

    plot_pieces(pieces.PIECES)