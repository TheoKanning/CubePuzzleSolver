import itertools
import numpy as np

import pieces

PIECES = [
    ((0, 0, 0), (1, 1, 0), (1, 2, 1)),
    ((0, 0, 0), (0, 1, 0), (1, 0, 1)),
    ((0, 0, 0), (1, 0, 0), (2, 0, 0)),
    ((0, 0, 0), (1, 1, 0), (2, 1, 1)),
    ((0, 0, 0), (0, 1, 0), (1, 2, 0)),
    ((0, 0, 0), (1, 0, 0), (0, 1, 0)),
    ((0, 0, 0), (0, 1, 1), (1, 1, 0)),
    ((0, 0, 0), (1, 1, 0), (2, 2, 0)),
    ((0, 0, 0), (1, 1, 0), (0, 2, 0)),
]


def ind_to_xyz(ind):
    z, ind = divmod(ind, 9)
    y, x = divmod(ind, 3)
    return (x, y, z)


def xyz_to_ind(xyz):
    x, y, z = xyz
    return 9*z + 3*y + x


def piece_key(piece):
    """
    Returns a string containing the index for each cube in this piece.
    This can be used as a key to find unique configurations
    """
    return " ".join([str(pieces.xyz_to_ind(point)) for point in piece])


def get_all_configurations(piece):
    """
    Given a list of xyz tuples, return a list of all possible unique configurations
    """
    from scipy.spatial.transform import Rotation as R

    rotations = list(itertools.product([0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270]))
    translations = list(itertools.product([0, 1, 2], [0, 1, 2], [0, 1, 2]))

    configurations = {}

    for r in rotations:
        rotation = R.from_euler("xyz", r, degrees=True)
        rotated = np.rint(rotation.apply(piece)).astype('int')

        for t in translations:
            c = rotated + t

            if c.min() >= 0 and c.max() <= 2:
                key = piece_key(c)
                configurations[key] = c

    return list(configurations.values())
