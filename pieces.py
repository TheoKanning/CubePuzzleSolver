import itertools
from collections import namedtuple
from typing import List, Set

import numpy as np

Point = namedtuple("Point", ["x", "y", "z"])
Edge = Set[Point]


def point_to_ind(point: Point) -> int:
    """
    Takes a point between (0, 0, 0) and (2, 2, 2) and returns a unique int between 0 and 26
    """
    x, y, z = point
    return 9 * z + 3 * y + x


class Piece:
    def __init__(self, points: List[Point], colors: List[str]):
        self.points = points
        self.indices = [point_to_ind(p) for p in points]
        self.edges = self._calculate_edges(points)
        self.colors = colors

    def _calculate_edges(self, points) -> List[Edge]:
        """
        Calculates if any of piece's point share two corners
        These special edges must be tracked so that pieces don't share them
        """

        def corners(point: Point) -> Set[Point]:
            # points are indexed from their lowest corners, so get their corners by adding 1 in each direction
            corner_points = itertools.product((point[0], point[0] + 1), (point[1], point[1] + 1),
                                              (point[2], point[2] + 1))
            corner_points = [Point(*p) for p in corner_points]
            return set(corner_points)

        edges = []

        for p1, p2 in [(0, 1), (0, 2), (1, 2)]:
            p1_corners = corners(points[p1])
            p2_corners = corners(points[p2])

            intersection = p1_corners.intersection(p2_corners)

            if len(intersection) == 2:
                edges.append(intersection)

        return edges


PIECES = [
    Piece(points=[Point(0, 0, 0), Point(1, 1, 0), Point(1, 2, 1)],
          colors=['g', 'r', 'g']),
    Piece(points=[Point(0, 0, 0), Point(0, 1, 0), Point(1, 0, 1)],
          colors=['r', 'r', 'r']),
    Piece(points=[Point(0, 0, 0), Point(1, 0, 0), Point(2, 0, 0)],
          colors=['r', 'r', 'r']),
    Piece(points=[Point(0, 0, 0), Point(1, 1, 0), Point(2, 1, 1)],
          colors=['r', 'g', 'g']),
    Piece(points=[Point(0, 0, 0), Point(0, 1, 0), Point(1, 2, 0)],
          colors=['r', 'g', 'g']),
    Piece(points=[Point(0, 0, 0), Point(1, 0, 0), Point(0, 1, 0)],
          colors=['r', 'g', 'r']),
    Piece(points=[Point(0, 0, 0), Point(0, 1, 1), Point(1, 1, 0)],
          colors=['g', 'g', 'g']),
    Piece(points=[Point(0, 0, 0), Point(1, 1, 0), Point(2, 2, 0)],
          colors=['r', 'g', 'r']),
    Piece(points=[Point(0, 0, 0), Point(1, 1, 0), Point(0, 2, 0)],
          colors=['g', 'g', 'g']),
]


def get_internal_edges() -> List[Edge]:
    """
    Returns a list of all edges inside the 3x3 cube
    Only these edges need to be considered when solving
    """
    edges = {}
    internal_points = itertools.product([1, 2], [1, 2], [1, 2])
    internal_points = [Point(*p) for p in internal_points]

    for point in internal_points:
        for axis in range(3):
            for delta in [-1, 1]:
                new_point = list(point)
                new_point[axis] += delta
                new_point = Point(*new_point)
                key = edge_key({point, new_point})
                edges[key] = {tuple(point), tuple(new_point)}

    return list(edges.values())


def piece_key(piece: Piece) -> str:
    """
    Returns a string containing the index for each cube in this piece.
    This can be used as a key to find unique configurations
    """
    indices = [point_to_ind(point) for point in piece.points]
    indices.sort()
    indices = map(str, indices)
    return " ".join(indices)


def edge_key(edge: Edge) -> str:
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
    from scipy.spatial.transform import Rotation

    rotations = list(itertools.product([0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270]))
    translations = list(itertools.product([0, 1, 2], [0, 1, 2], [0, 1, 2]))

    configurations = {}

    for r in rotations:
        rotation = Rotation.from_euler("xyz", r, degrees=True)
        rotated_points = np.rint(rotation.apply(piece.points)).astype('int')

        for t in translations:
            new_points = rotated_points + t

            if new_points.min() >= 0 and new_points.max() <= 2:
                new_piece = Piece(points=new_points, colors=piece.colors)
                configurations[piece_key(new_piece)] = new_piece

    return list(configurations.values())
