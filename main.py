# or-tools

import graph
import pieces
import numpy as np

piece = pieces.PIECES[2]
# print(piece)
piece = pieces.get_all_configurations(piece)[40]
# print(piece)
graph.plot_pieces(pieces.PIECES)
# graph.plot_piece(piece)
