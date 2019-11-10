"""
CSP representation for 8-Queens Problem
Define a variable for each row in chess board. Every variable holds the column index that
the queen is placed on. With this representation, we do not need to check if two queens
are on same row.
Created on Feb 7, 2011

@author: goker
"""

import itertools

from aiama.search import CSP


def check_constraints(state):
    # for every pair of queen
    for s1, s2 in itertools.combinations(state.assignments.keys(), 2):
        # if 2 queens are on the same column
        if state.assignments[s1] == state.assignments[s2]:
            return False
        # if 2 queens are attacking each other diagonally
        rowDiff = ord(s2) - ord(s1)
        if state.assignments[s1] + rowDiff == state.assignments[s2] or state.assignments[s1] - rowDiff == \
                state.assignments[s2]:
            return False
    return True


def forward_checking(state, val):
    """
    Return a dictionary of illegal values for each unassigned variable 
    """
    # find unassigned variables
    unassignedVars = list(state.varList)
    [unassignedVars.remove(k) for k in state.assignments.keys()]
    # nextVariable is being assigned right now it is not an unassigned variable
    unassignedVars.remove(state.nextVariable)
    # dictionary that holds values to be removed for each variable
    removeVals = {}
    # for every unassigned variable, construct a list of values to be removed    
    for v in unassignedVars:
        # two queens can't be on same column
        vals = [val]
        # add diagonal positions if they are inside boundaries of chess board
        rowDiff = ord(v) - ord(state.nextVariable)
        if 0 < val + rowDiff <= 8:
            vals.append(val + rowDiff)
        if 0 < val - rowDiff <= 8:
            vals.append(val - rowDiff)
        removeVals[v] = vals
    return removeVals


if __name__ == '__main__':
    varsAndDomains = {('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'): [1, 2, 3, 4, 5, 6, 7, 8]}
    csp = CSP(varsAndDomains, [check_constraints], forward_checking)
    node = csp.solve()
    print(node)
