from collections import namedtuple
import itertools
import numpy as np

from typing import List

class Piece:
  def __init__(self, points: List[tuple], edges: List[tuple], colors: List[str]):
    self.points = points
    self.indices = [xyz_to_ind(p) for p in points]
    self.edges = edges
    self.colors = colors


PIECES = [
    Piece(points=((0, 0, 0), (1, 1, 0), (1, 2, 1)), 
          edges=[((1, 1, 0), (1, 1, 1)), ((1, 2, 1), (2, 2, 1))], 
          colors=['g', 'r', 'g']),
    Piece(points=((0, 0, 0), (0, 1, 0), (1, 0, 1)), 
          edges=[((1, 1, 1), (1, 2, 1))], 
          colors=['r', 'r', 'r']),
    Piece(points=((0, 0, 0), (1, 0, 0), (2, 0, 0)), 
          edges=[], 
          colors=['r', 'r', 'r']),
    Piece(points=((0, 0, 0), (1, 1, 0), (2, 1, 1)), 
          edges=[((1, 1, 0), (1, 1, 1)), ((2, 1, 1), (2, 2, 1))], 
          colors=['r', 'g', 'g']),
    Piece(points=((0, 0, 0), (0, 1, 0), (1, 2, 0)), 
          edges=[((1, 2, 0), (1, 2, 1))], 
          colors=['r', 'g', 'g']),
    Piece(points=((0, 0, 0), (1, 0, 0), (0, 1, 0)), 
          edges=[], 
          colors=['r', 'g', 'r']),
    Piece(points=((0, 0, 0), (0, 1, 1), (1, 1, 0)), 
          edges=[((1, 1, 0), (1, 1, 1)), ((0, 1, 1), (1, 1, 1)), ((1, 1, 1), (1, 2, 1))], 
          colors=['g', 'g', 'g']),
    Piece(points=((0, 0, 0), (1, 1, 0), (2, 2, 0)), 
          edges=[((1, 1, 0), (1, 1, 1)), ((2, 2, 0), (2, 2, 1))], 
          colors=['r', 'g', 'r']),
    Piece(points=((0, 0, 0), (1, 1, 0), (0, 2, 0)), 
          edges=[((1, 1, 0), (1, 1, 1)), ((1, 2, 0), (1, 2, 1))], 
          colors=['g', 'g', 'g']),
]


def ind_to_xyz(ind: int) -> tuple:
    z, ind = divmod(ind, 9)
    y, x = divmod(ind, 3)
    return (x, y, z)


def xyz_to_ind(xyz: tuple):
    x, y, z = xyz
    return 9*z + 3*y + x


def piece_key(piece: Piece) -> str:
    """
    Returns a string containing the index for each cube in this piece.
    This can be used as a key to find unique configurations
    """
    indices = [str(xyz_to_ind(point)) for point in piece.points]
    indices.sort()
    return " ".join(indices)


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
        rotated = np.rint(rotation.apply(piece.points)).astype('int')

        for t in translations:
            new_points = rotated + t

            if new_points.min() >= 0 and new_points.max() <= 2:
                new_piece = Piece(points=new_points, edges=piece.edges, colors=piece.colors)
                configurations[piece_key(new_piece)] = new_piece

    return list(configurations.values())
