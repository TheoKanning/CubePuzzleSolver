from ortools.linear_solver import pywraplp

num_pieces = len(piece_configurations)
solver = pywraplp.Solver.CreateSolver('SCIP')

# each variable is a piece/configuration combo
# if 1 then the piece is in that configurations
variables = {}

for p in range(num_pieces):
  num_configurations = len(piece_configurations[p])
  variables[p] = [solver.IntVar(0, 1, f"{p}-{c}") for c in range(num_configurations)]

# each piece can only have one configuration
for p, piece_vars in enumerate(variables.values()):
  ct = solver.Constraint(1, 1, f"piece {p}")

  for var in piece_vars:
    ct.SetCoefficient(var, 1)

# each square can only be occupied by one piece
for s in range(27):
  ct = solver.Constraint(1, 1, f"square {s}")
  for p, piece_vars in enumerate(variables.values()):
    for c, var in enumerate(piece_vars):
      if s in piece_configurations[p][c]:
        ct.SetCoefficient(var, 1)

# objective is to place all pieces
objective = solver.Objective()
objective.SetMaximization()
for piece_vars in variables.values():
  for var in piece_vars:
    objective.SetCoefficient(var, 1)

solver.Solve()

print(objective.Value())

# print results
solution = []
for p, piece_vars in enumerate(variables.values()):
  for c, var in enumerate(piece_vars):
    if var.solution_value() == 1:
      solution.append(piece_configurations[p][c])
      break

solution.sort(key=sum)
solution = [[ind_to_xyz(i) for i in piece] for piece in solution]
for p in range(num_pieces):
  plot_pieces(solution[:p+1])
