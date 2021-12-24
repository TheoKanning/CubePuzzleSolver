import itertools
import numpy as np

PIECES = [
    ((0, 0, 0), (1, 1, 0), (1, 2, 1)),
    ((0, 0, 0), (0, 1, 0), (1, 0, 1)),
]


def ind_to_xyz(ind):
    z, ind = divmod(ind, 9)
    y, x = divmod(ind, 3)
    return (x, y, z)


def xyz_to_ind(xyz):
    x, y, z = xyz
    return 9*z + 3*y + x


def get_all_configurations(piece):
    """
    Given a list of xyz tuples, return a list of all possible unique configurations
    """
    from scipy.spatial.transform import Rotation as R

    rotations = list(itertools.product([0, 90, 180, 270], [0, 90, 180, 270], [0, 90, 180, 270]))
    translations = list(itertools.product([0, 1, 2], [0, 1, 2], [0, 1, 2]))

    configurations = []
    count = 0

    for r in rotations:
        rotation = R.from_euler("xyz", r, degrees=True)
        rotated = np.rint(rotation.apply(piece)).astype('int')

        for t in translations:
            c = rotated + t

            if ((0 <= c) & (c < 3)).all():
                configurations.append(c)
            count += 1

    print(count)
    return configurations
