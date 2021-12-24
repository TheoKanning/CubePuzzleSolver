# remove duplicates
# or-tools

import graph
import pieces
import numpy as np

piece = pieces.PIECES[0]
print(piece)
piece = pieces.get_all_configurations(piece)[50]
print(piece)
graph.plot_piece(piece)
