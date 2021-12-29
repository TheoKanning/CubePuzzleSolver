# todo add point namedtuple to prevent list hashing issues
# todo edge tests

import graph
import pieces
import solve

piece_configurations = [pieces.get_all_configurations(p) for p in pieces.PIECES]
edges = pieces.get_internal_edges()

solution = solve.solve(piece_configurations, edges)

solution.sort(key=lambda x: sum(x.indices))
for p in range(9):
    graph.plot_pieces(solution[:p + 1])
