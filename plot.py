from typing import List

import matplotlib.pyplot as plt
import numpy as np

from pieces import Piece


def plot_piece(piece: Piece):
    plot_pieces([piece])


def plot_pieces(pieces: List[Piece]):

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    _format_axes(ax)

    voxels, colors, edge_colors = _pieces_to_voxel(pieces)
    ax.voxels(voxels, facecolors=colors, edgecolors=edge_colors)

    plt.show()


def plot_solution(pieces: List[Piece]):
    fig, axs = plt.subplots(3, 3, subplot_kw={'projection': '3d'})

    step = 1
    for row in axs:
        for ax in row:
            _format_axes(ax)
            voxels, colors, edge_colors = _pieces_to_voxel(pieces[:step])
            ax.voxels(voxels, facecolors=colors, edgecolors=edge_colors)
            ax.set_title(f"Step {step}")
            step += 1

    plt.show()


def plot_edges(piece: Piece):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    _format_axes(ax)

    def diff(p1, p2, ind):
        d = p2[ind] - p1[ind]
        return 0.1 if d == 0 else d

    for p1, p2 in piece.edges:
        diffs = [diff(p1, p2, i) for i in range(3)]
        ax.bar3d(*p1, *diffs, color='b')

    plt.show()


def _pieces_to_voxel(pieces: List[Piece]):
    """
    Returns voxel, color, and edge_color data for the given pieces
    All piece but the last will appear grayed out
    """
    axes = [3, 3, 3]

    voxels = np.zeros(axes, dtype=bool)

    colors = np.empty(axes + [4], dtype=np.float32)
    edge_colors = np.empty(axes + [4], dtype=np.float32)

    colors[:] = [0.7, 0.7, 0.7, 0.4]  # light gray background
    edge_colors[:] = [0, 0, 0, 0]  # none

    for p, piece in enumerate(pieces):
        for point, color in zip(piece.points, piece.colors):
            x, y, z = point
            voxels[x, y, z] = 1

            if p == len(pieces) - 1:
                # highlight last piece
                edge_colors[x, y, z, :] = [0.1, 0.1, 0.1, 1]
                if color == 'r':
                    colors[x, y, z, :] = [1, 0, 0, 1]
                else:
                    colors[x, y, z, :] = [.7, 0.7, 0.7, 1]

    return voxels, colors, edge_colors


def _format_axes(ax):
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels([])
    ax.set_xlim(0, 3)

    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels([])
    ax.set_ylim(0, 3)

    ax.set_zticks([0, 1, 2])
    ax.set_zticklabels([])
    ax.set_zlim(0, 3)
