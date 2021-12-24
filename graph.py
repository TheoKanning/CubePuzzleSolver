import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_piece(piece):
    axes = [3, 3, 3]

    data = np.zeros(axes, dtype=np.bool)
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

if __name__ == "__main__":
    import pieces

    plot_piece(pieces.PIECES[0])