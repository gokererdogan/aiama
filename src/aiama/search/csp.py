# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
"""
AIAMA Chapter 3: Solving Problems By Searching
General definition of a Constraint Satisfaction Problem
Created on Feb 6, 2011

@author: goker
"""

import copy

from .search import State, SearchProblem, Operator


class CSPState(State):
    """
    Search state for a CSP. 
    Assignments hold assigned values for each variable
    """

    def __init__(self, variables, domains, nextVariable, assignments, constraints, forwardCheckingFunc):
        """
        Initialize CSP state.
        Variables is a list of tuples containing variables
        Domains is a dictionary containing variable-domain pairs
        Next variable is the variable that will be assigned next
        Assignments is a dictionary containing values assigned for each variable
        constraints is a list of functions checking constraints on CSPState instances
        e.g. variables: [(a,b),(c,d)] domains: [{a:[1,2,3], b:[1,2,3]}, {c:[5,6,7], d:[5,6,7]}
        """
        State.__init__(self)
        self.variables = variables
        self.domains = domains
        self.nextVariable = nextVariable
        self.assignments = assignments
        self.constraints = constraints
        self.forwardCheckingFunction = forwardCheckingFunc
        self.varList = []
        for vg in self.variables:
            for v in vg:
                self.varList.append(v)

    def __repr__(self):
        return repr(self.assignments)

    def __hash__(self):
        return hash(tuple(self.assignments.values()))

    def __eq__(self, other):
        return self.assignments == other.assignments

    def assign_value_to_next_variable(self):
        # we have assigned value to all variables, there are no new states
        if self.nextVariable is None:
            return []
        varindex = self.varList.index(self.nextVariable)
        nextVar = self.varList[varindex + 1] if varindex + 1 < len(self.varList) else None
        nstates = []
        for d in self.domains[self.nextVariable]:
            nstate = CSPState(self.variables, copy.deepcopy(self.domains), nextVar, copy.deepcopy(self.assignments),
                              self.constraints, self.forwardCheckingFunction)
            nstate.assignments[self.nextVariable] = d

            if self.forwardCheckingFunction is not None:
                # forward checking
                # get values to remove from unassigned variables
                removeVals = self.forwardCheckingFunction(self, d)
                # remove values from each variable's domain
                for unassignedVar in removeVals.keys():
                    [nstate.domains[unassignedVar].remove(v) for v in removeVals[unassignedVar] if
                     v in nstate.domains[unassignedVar]]

            nstates.append(nstate)
        return nstates

    def is_goal_state(self):
        # if all variables are not assigned, return false        
        if len(self.assignments.keys()) != len(self.varList):
            return False
        # check every constraint
        return self.is_legal()

    def is_legal(self):
        # check every constraint
        for constraint in self.constraints:
            if not constraint(self):
                return False
        return True


class CSP:
    """
    General Definition of a CSP
    """

    def __init__(self, varsAndDomains, constraints, forwardCheckingFunc=None):
        """
        Initialize CSP
        varsAndDomains is a dictionary of variables tuples and corresponding domain tuples
        constraints is a list of functions checking constraints on CSPState instances
        e.g. varsAndDomains {('A','B'):(0,1,2,3)}
        """
        self.varsAndDomains = varsAndDomains
        self.variables = list(varsAndDomains.keys())
        self.domains = {}
        for varsT in self.variables:
            for v in varsT:
                self.domains[v] = list(self.varsAndDomains[varsT])
        self.constraints = constraints
        self.forwardCheckingFunc = forwardCheckingFunc

    def solve(self):
        initialState = CSPState(self.variables, self.domains, self.variables[0][0], {}, self.constraints,
                                self.forwardCheckingFunc)
        operators = [Operator("Assign Value", self.__assign_value_to_variable)]
        problem = SearchProblem(initialState, operators, self.__goal_test)
        node = problem.depth_first_search()
        return node

    @staticmethod
    def __assign_value_to_variable(state):
        return state.assign_value_to_next_variable()

    @staticmethod
    def __goal_test(state):
        return state.is_goal_state()

