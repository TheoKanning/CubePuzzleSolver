import matplotlib.pyplot as plt
import numpy as np


def plot_piece(piece: Piece, plot_edges=False):
    plot_pieces([piece], plot_edges)


def plot_pieces(pieces: List[Piece], plot_edges=False):
    axes = [3, 3, 3]

    data = np.zeros(axes, dtype=bool)

    colors = np.empty(axes + [4], dtype=np.float32)
    edge_colors = np.empty(axes + [4], dtype=np.float32)

    colors[:] = [0.7, 0.7, 0.7, 0.4]  # light gray background
    edge_colors[:] = [0, 0, 0, 0]  # none
    edges = []

    for p, piece in enumerate(pieces):
        for point, color in zip(piece.points, piece.colors):
            x, y, z = point
            data[x, y, z] = 1

            if p == len(pieces) - 1:
                # highlight last piece
                edge_colors[x, y, z, :] = [0.1, 0.1, 0.1, 1]
                if color == 'r':
                    colors[x, y, z, :] = [1, 0, 0, 0.9]
                else:
                    colors[x, y, z, :] = [.7, 0.7, 0.7, 0.9]

            edges = piece.edges

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def diff(p1, p2, ind):
        d = p2[ind] - p1[ind]
        return 0.1 if d == 0 else d

    if plot_edges:
        for p1, p2 in piece.edges:
            diffs = [diff(p1, p2, i) for i in range(3)]
            ax.bar3d(*p1, *diffs, color='b')
    else:
        ax.voxels(data, facecolors=colors, edgecolors=edge_colors)

    ax.set_xticks([0, 1, 2])
    ax.set_xlim(0, 3)
    ax.set_yticks([0, 1, 2])
    ax.set_ylim(0, 3)
    ax.set_zticks([0, 1, 2])
    ax.set_zlim(0, 3)
    plt.show()
