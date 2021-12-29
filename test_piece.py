import pytest

import pieces


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
    actual = pieces.point_to_ind(xyz)
    assert actual == expected


@pytest.mark.parametrize(
    ["points", "expected"],
    [
        [((0, 0, 0), (1, 1, 0), (1, 2, 1)), "0 4 16"],
        [((0, 0, 0), (0, 1, 0), (1, 0, 1)), "0 3 10"]
    ]
)
def test_piece_key(points, expected):
    piece = pieces.Piece(points=points, colors=[])
    actual = pieces.piece_key(piece)
    assert actual == expected


@pytest.mark.parametrize(
    ["points", "expected"],
    [
        [((1, 1, 0), (1, 1, 1)), "110 111"],
        [((0, 1, 0), (0, 0, 0)), "000 010"]
    ]
)
def test_edge_key(points, expected):
    actual = pieces.edge_key(points)
    assert actual == expected


@pytest.mark.parametrize(
    ["points", "expected"],
    [
        [((0, 0, 0), (1, 1, 0), (1, 2, 1)), ["110 111", "121 221"]],
        [((0, 0, 0), (0, 1, 0), (1, 0, 1)), ["101 111"]],
        [((0, 0, 0), (1, 0, 0), (2, 0, 0)), []]
    ]
)
def test_calculate_edges(points, expected):
    piece = pieces.Piece(points=points, colors=[])
    actual = [pieces.edge_key(e) for e in piece.edges]
    assert actual == expected

