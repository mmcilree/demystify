#!/usr/bin/env python3
import copy
import sys
import os
import logging

# Let me import puzsmt from one directory up
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import puzsmt
import puzsmt.base
import puzsmt.internal
import puzsmt.MUS
import puzsmt.solve
import puzsmt.prettyprint
import demystify.buildpuz

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(name)s:%(relativeCreated)d:%(message)s"
)

puzsmt.config.LoadConfigFromDict({"cores": 24, "smallRepeats": 5, "repeats": 20})


# Make a matrix of variables (we can make more than one)
vars = puzsmt.base.VarMatrix(lambda t: (t[0] + 1, t[1] + 1), (9, 9), range(1, 9 + 1))

# Build the puzzle (we can pass multiple matrices, depending on the puzzle)
puz = puzsmt.base.Puzzle([vars])

# https://www.youtube.com/watch?v=U99ZFz_X4TU

thermometers = [
    [(0,2),(0,3),(1,3),(1,2),(2,2),(2,3)],
    [(2,4),(2,5),(1,5),(1,4),(0,4),(0,5)],
    [(1,7),(0,7),(0,8),(1,8),(2,8)],
    [(1,7),(0,6),(1,6),(2,6)],

    [(2,1),(3,0)],
    
    [(3,2),(3,1),(4,0),(5,1),(5,2)],
    [(4,3),(4,4),(4,5)],
    [(4,3),(4,4),(3,4)],
    [(4,3),(4,4),(5,4),(5,5)],
    [(5,3),(6,2)],
    [(5,8),(5,7),(4,6),(3,7),(3,8)],
    
    [(6,1),(6,0),(7,0),(7,1),(8,1),(8,0)],
    [(7,2),(8,2),(8,3),(7,3)],

    [(7,5),(8,5),(8,4),(7,4),(6,5)],
    [(8,6),(8,7),(7,6),(7,7)]
]


constraints = []
constraints += demystify.buildpuz.basicSudoku(vars)
for t in thermometers:
    constraints += demystify.buildpuz.thermometer(vars, t)

puz.addConstraints(constraints)


solver = puzsmt.internal.Solver(puz)

sudoku = [[None] * 9 for _ in range(9)]


# First, we turn it into an assignment (remember technically an assignment is a list of variables, so we pass [sudoku])

sudokumodel = puz.assignmentToModel([sudoku])

fullsolution = solver.solveSingle(sudokumodel)

# Then we 'add' all the assignments that we know (this is what we can undo later with a 'pop')
for s in sudokumodel:
    solver.addLit(s)

# The 'puzlits' are all the booleans we have to solve
# Start by finding the ones which are not part of the known values
puzlits = [p for p in fullsolution if p not in sudokumodel]

MUS = puzsmt.MUS.CascadeMUSFinder(solver)

trace = puzsmt.solve.html_solve(sys.stdout, solver, puzlits, MUS)

print("Minitrace: ", [(s, mins[0], len(mins)) for (s, mins) in trace])


logging.info("Finished")
logging.info("Full Trace %s", trace)
