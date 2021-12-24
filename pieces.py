# returns list of pieces

def ind_to_xyz(ind):
    z, ind = divmod(ind, 9)
    y, x = divmod(ind, 3)
    return (x, y, z)


def xyz_to_ind(xyz):
    x, y, z = xyz
    return 9*z + 3*y + x

PIECES = [
    ((0, 0, 0), (1, 1, 0), (1, 2, 1)),
    ((0, 0, 0), (0, 1, 0), (1, 0, 1)),
]
