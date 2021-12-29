import itertools
from typing import List, Tuple

import numpy as np


def ind_to_xyz(ind: int) -> tuple:
    z, ind = divmod(ind, 9)
    y, x = divmod(ind, 3)
    return x, y, z


def xyz_to_ind(xyz: tuple):
    x, y, z = xyz
    return 9 * z + 3 * y + x


class Piece:
    def __init__(self, points: List[tuple], colors: List[str]):
        self.points = points
        self.indices = [xyz_to_ind(p) for p in points]
        self.edges = self._calculate_edges(points)
        self.colors = colors

    def _calculate_edges(self, points) -> List[Tuple[Tuple]]:
        """
        Calculates if any of piece's point share two corners
        These special edges must be tracked so that pieces don't share them
        """

        def corners(point: Tuple):
            # points are indexed from their lowest corners, so get their corners by adding 1 in each direction
            return set(itertools.product((point[0], point[0] + 1), (point[1], point[1] + 1), (point[2], point[2] + 1)))

        edges = []

        for p1, p2 in [(0, 1), (0, 2), (1, 2)]:
            p1_corners = corners(points[p1])
            p2_corners = corners(points[p2])

            intersection = p1_corners.intersection(p2_corners)

            if len(intersection) == 2:
                edges.append(intersection)

        return edges


PIECES = [
    Piece(points=((0, 0, 0), (1, 1, 0), (1, 2, 1)),
          colors=['g', 'r', 'g']),
    Piece(points=((0, 0, 0), (0, 1, 0), (1, 0, 1)),
          colors=['r', 'r', 'r']),
    Piece(points=((0, 0, 0), (1, 0, 0), (2, 0, 0)),
          colors=['r', 'r', 'r']),
    Piece(points=((0, 0, 0), (1, 1, 0), (2, 1, 1)),
          colors=['r', 'g', 'g']),
    Piece(points=((0, 0, 0), (0, 1, 0), (1, 2, 0)),
          colors=['r', 'g', 'g']),
    Piece(points=((0, 0, 0), (1, 0, 0), (0, 1, 0)),
          colors=['r', 'g', 'r']),
    Piece(points=((0, 0, 0), (0, 1, 1), (1, 1, 0)),
          colors=['g', 'g', 'g']),
    Piece(points=((0, 0, 0), (1, 1, 0), (2, 2, 0)),
          colors=['r', 'g', 'r']),
    Piece(points=((0, 0, 0), (1, 1, 0), (0, 2, 0)),
          colors=['g', 'g', 'g']),
]


def get_internal_edges():
    edges = {}
    internal_points = itertools.product([1, 2], [1, 2], [1, 2])

    for point in internal_points:
        for axis in range(3):
            for delta in [-1, 1]:
                new_point = list(point)
                new_point[axis] += delta
                key = edge_key((point, new_point))
                edges[key] = {tuple(point), tuple(new_point)}

    return list(edges.values())


def piece_key(piece: Piece) -> str:
    """
    Returns a string containing the index for each cube in this piece.
    This can be used as a key to find unique configurations
    """
    indices = [xyz_to_ind(point) for point in piece.points]
    indices.sort()
    indices = map(str, indices)
    return " ".join(indices)


def edge_key(edge: Tuple[Tuple]):
    """
    Edges go from 0 to 3, so piece index will not work
    """
    points = ["".join([str(x) for x in point]) for point in edge]
    points.sort()
    return " ".join(points)


def get_all_configurations(piece: Piece) -> List[Piece]:
    """
    Given a list of xyz tuples, return a list of all possible unique configurations
    """
    from scipy.spatial.transform import Rotation as R

    rotations = list(itertools.product([0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270]))
    translations = list(itertools.product([0, 1, 2], [0, 1, 2], [0, 1, 2]))

    configurations = {}

    for r in rotations:
        rotation = R.from_euler("xyz", r, degrees=True)
        rotated_points = np.rint(rotation.apply(piece.points)).astype('int')

        for t in translations:
            new_points = rotated_points + t

            if new_points.min() >= 0 and new_points.max() <= 2:
                new_piece = Piece(points=new_points, colors=piece.colors)
                configurations[piece_key(new_piece)] = new_piece

    return list(configurations.values())
