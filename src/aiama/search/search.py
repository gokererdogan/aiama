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
General definition of a search problem and implementation
of various search methods
Goker 03.02.2011
"""
import sys


class State:
    """
    Class for defining search space state. Subclass this class to define a
    specific state class for a problem
    """

    def __init__(self):
        pass

    def __eq__(self, other):
        pass

    def __repr__(self):
        pass

    def __hash__(self):
        """
        Implement a hashing method for state to be able to store states in a dictionary for
        checking repeated states
        """
        pass

    def is_legal(self):
        """
        check if state is a legal state
        Override this function in subclasses and implement a function that returns
        true if state is a legal state for the given problem, false otherwise
        """
        pass


class Operator:
    """
    Class for operator for a search problem.
    """

    def __init__(self, name, func, cost=0):
        """
        Pass name, cost of the operator and function that applies the operator to a given state to constructor
        """
        self.name = name
        self.func = func
        self.cost = cost

    def apply_operator(self, state):
        """
        Apply operator to state and return new state
        """
        return self.func(state)

    def __repr__(self):
        return self.name


class SearchTreeNode:
    """
    Class defining a node in search tree
    """

    def __init__(self, state, parent=None, appliedOperator=None, depth=0, pathCost=0, heuristicValue=-1, f=0):
        """
        Pass state the node corresponds, its parent node,
        applied operator to reach this node, depth of the node and total path cost to this node
        """
        self.state = state
        self.parent = parent
        self.appliedOperator = appliedOperator
        self.depth = depth
        self.pathCost = pathCost
        self.heuristicValue = heuristicValue
        self.f = f

    def __repr__(self):
        if self.heuristicValue != -1:
            return "State: %s, Depth: %d, Path Cost: %f, Heuristic Value: %f, Applied Operator: %s" % (
                self.state, self.depth, self.pathCost, self.heuristicValue, self.appliedOperator)
        else:
            return "State: %s, Depth: %d, Path Cost: %f, Applied Operator: %s" % (
                self.state, self.depth, self.pathCost, self.appliedOperator)


class SearchProblem:
    """
    Class defining a search problem with its initial state,
    operators, goal test and path cost function
    """

    def __init__(self, initialState, operators, goalTestFunc, pathCostFunc=None, heuristicFunctions=None):
        """
        Pass initial state which is the root node for search tree, operators that can be applied to states,
        goal test function and path cost function heuristicFunctions are a list of functions that give heuristic
        values for any state heuristic functions are assumed to be admissible. if multiple heuristic functions are
        given maximum of them are used for each state To ensure monotonicity of f cost, pathmax is used. (if f cost
        for a node is smaller than its parent, its parent's cost is used)
        """
        self.initialState = initialState
        self.operators = operators
        self.goalTestFunc = goalTestFunc
        self.pathCostFunc = pathCostFunc
        self.heuristicFunctions = heuristicFunctions

    def general_search(self, queuingFunc, maxDepth=0):
        """
        Search problem to find a solution, use queuingFunc to add new nodes to fringe
        Returns node that reached goal state
        """
        # fringe
        nodes = []
        # add initial state to queue
        nodes.append(SearchTreeNode(self.initialState))
        # add initial state to generated states list
        self.generatedStates = {}
        self.generatedStates[self.initialState] = 1

        # update root node's heuristic value and f cost
        f, g, h = self.__get_node_cost_values(nodes[0])
        nodes[0].heuristicValue = h
        nodes[0].f = h

        while True:
            # if there are nodes to be expanded
            if len(nodes) != 0:
                # get next node from queue
                node = nodes.pop(0)

                if self.goalTestFunc(node.state):
                    return node
                # add new nodes to queue
                nodes = queuingFunc(nodes, self.__expand(node, maxDepth))
            else:  # if fringe is empty, search fails
                return None

    @staticmethod
    def get_solution_path(solutionNode):
        """
        Return a list containing the nodes traversed to reach solution
        """
        solution = []
        node = solutionNode
        while node.parent is not None:
            solution.insert(0, node)
            node = node.parent
        solution.insert(0, node)
        return solution

    def __expand(self, node, depthLimit=0):
        """
        Expand node and generate new child nodes
        """
        nnodes = []

        # apply each operator to state in node
        for operator in self.operators:
            nstates = operator.apply_operator(node.state)
            for nstate in nstates:
                # add node to expanded nodes list if it is a legal state and not generated before
                if nstate.is_legal() and nstate not in self.generatedStates:

                    # create a node from the expanded state
                    nnode = SearchTreeNode(nstate, node, operator, node.depth + 1)

                    # get pathCost and heuristic value for node
                    f, g, h = self.__get_node_cost_values(nnode)
                    nnode.pathCost = g
                    nnode.heuristicValue = h
                    nnode.f = f

                    # if a depth limit is specified, check it
                    if depthLimit == 0 or nnode.depth < depthLimit:
                        nnodes.append(nnode)
                        self.generatedStates[nstate] = 1
        return nnodes

    def __get_node_cost_values(self, node):
        # if heuristic functions are provided, use their maximum as h value
        h = -1
        g = 0

        # calculate path cost for new node and update it
        if node.parent is not None:
            if self.pathCostFunc is None:
                g = node.parent.pathCost + 1
            else:  # if problem contains a path cost function, get the path cost from it
                g = node.parent.pathCost + self.pathCostFunc(node.parent.state, node.state)

        f = g
        if self.heuristicFunctions is not None:
            for f in self.heuristicFunctions:
                if f(node.state) > h:
                    h = f(node.state)

            # if f cost of node is smaller than parent's, use parent's f cost to ensure monotonicity
            if node.parent is not None:
                parentf = node.parent.f
                f = g + h
                if f < parentf:
                    f = parentf

        return f, g, h

    def breadth_first_search(self):
        return self.general_search(QueuingFunction.enqueue_at_end)

    def uniform_cost_search(self):
        return self.general_search(QueuingFunction.sort_by_path_cost)

    def depth_first_search(self):
        return self.general_search(QueuingFunction.enqueue_at_front)

    def depth_limited_search(self, maxDepth):
        """
        Search problem to find a solution expanding until maxDepth
        Return node that reached goal state
        """
        return self.general_search(QueuingFunction.enqueue_at_front, maxDepth)

    def iterative_deepening_search(self, iterations=100):
        """
        Search solution starting from depth 1 to iterations using depth limited search
        Return node that reached goal state
        """
        for i in range(iterations):
            node = self.depth_limited_search(i + 1)
            if node is not None:
                return node
        return None

    def greedy_search(self):
        """
        Search solution by using heuristic value, choose the node with smallest h value at each step
        """
        if self.heuristicFunctions is None:
            raise AttributeError("Heuristic function(s) should be provided to use informed search methods")
        return self.general_search(QueuingFunction.sort_by_h)

    def a_star_search(self):
        """
        A* Search. Choose the node with smallest total  h + g at each step
        """
        if self.heuristicFunctions is None:
            raise AttributeError("Heuristic function(s) should be provided to use informed search methods")
        return self.general_search(QueuingFunction.sort_by_f)

    def iterative_deepening_a_star_search(self):
        """
        IDA*
        """
        # fringe
        # add initial state to queue
        nodes = [SearchTreeNode(self.initialState)]

        # update root node's heuristic value and f cost
        if self.heuristicFunctions is not None:
            f, g, h = self.__get_node_cost_values(nodes[0])
            nodes[0].heuristicValue = h
            nodes[0].f = h

        flimit = nodes[0].f
        # nextf is actually defined as static in dfsContour
        # since python does not have static variables, we pass it to function as a reference
        nextf = sys.maxsize
        while True:
            # look for solution with the current flimit
            # create dummy generated states to prevent errors in expand function
            self.generatedStates = {}
            solution, flimit = self.__dfs_contour(nodes[0], flimit, [nextf])
            if solution is not None:
                return solution
            if flimit == sys.maxsize:
                return None

    def __dfs_contour(self, node, flimit, nextf):
        if node.f > flimit:
            return None, node.f
        if self.goalTestFunc(node.state):
            return node, flimit
        childNodes = self.__expand(node)
        for n in childNodes:
            solution, newf = self.__dfs_contour(n, flimit, nextf)
            if solution is not None:
                return solution, flimit
            nextf[0] = nextf[0] if nextf[0] < newf else newf
        return None, nextf[0]


class QueuingFunction:
    """
    Class containing static queuing functions to use in search
    """

    @staticmethod
    def enqueue_at_end(l1, l2):
        """
        Appends l2 to end of l1
        """
        return l1 + l2

    @staticmethod
    def enqueue_at_front(l1, l2):
        """
        Appends l2 to start of l1
        """
        return l2 + l1

    @staticmethod
    def sort_by_path_cost(l1, l2):
        """
        Concatenates l1 and l2, sorts it by path cost
        """
        l = l1 + l2
        l.sort(key=lambda i: i.pathCost)
        return l

    @staticmethod
    def sort_by_h(l1, l2):
        """
        Concatenates l1 and l2, sorts it by heuristic value
        """
        l = l1 + l2
        l.sort(key=lambda i: i.heuristicValue)
        return l

    @staticmethod
    def sort_by_f(l1, l2):
        """
        Concatenates l1 and l2, sorts it by heuristic value + path cost
        """
        l = l1 + l2
        l.sort(key=lambda i: i.f)
        return l
