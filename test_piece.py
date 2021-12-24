import pytest

import pieces


@pytest.mark.parametrize(
    ["index", "expected"],
    [
        (0, (0, 0, 0)),
        (1, (1, 0, 0)),
        (3, (0, 1, 0)),
        (4, (1, 1, 0)),
        (5, (2, 1, 0)),
        (6, (0, 2, 0)),
        (8, (2, 2, 0)),
        (9, (0, 0, 1)),
        (14, (2, 1, 1)),
        (18, (0, 0, 2)),
        (24, (0, 2, 2)),
        (26, (2, 2, 2)),
    ]
)
def test_ind_to_xyz(index, expected):
    actual = pieces.ind_to_xyz(index)
    assert actual == expected


@pytest.mark.parametrize(
    ["xyz", "expected"],
    [
        ((0, 0, 0), 0),
        ((1, 0, 0), 1),
        ((0, 1, 0), 3),
        ((1, 1, 0), 4),
        ((2, 1, 0), 5),
        ((0, 2, 0), 6),
        ((2, 2, 0), 8),
        ((0, 0, 1), 9),
        ((2, 1, 1), 14),
        ((0, 0, 2), 18),
        ((0, 2, 2), 24),
        ((2, 2, 2), 26),
    ]
)
def test_xyz_to_ind(xyz, expected):
    actual = pieces.xyz_to_ind(xyz)
    assert actual == expected
