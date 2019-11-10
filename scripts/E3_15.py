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
Exercise 3.15
The chain problem (Figure 3.20) consists of various lengths of chain that must be recon-
figured into new arrangements. Operators can open one link and close one link. In the standard
form of the problem, the initial state contains four chains, each with three links. The goal state
consists of a single chain of 12 links in a circle. Set this up as a formal search problem and find
the shortest solution.

Created on Feb 3, 2011

@author: Goker
"""

import itertools

from aiama.search import Operator, SearchProblem, State

"""
chain Problem Definition
"""


class ChainState(State):
    """
    State representation for chain problem
    Each chain is represented by 2 numbers (e.g 0 left link, 1 right link)
    Links list stores where each link is connected to
    -1 2 means chain 1 is not connected from left and connected to left link of chain 2 from right
    """

    def __init__(self, links):
        State.__init__(self)
        self.links = links
        self.nchains = len(links) // 2

    def __eq__(self, other):
        return self.links == other.links

    def __repr__(self):
        return repr(self.links)

    def __hash__(self):
        return hash(tuple(self.links))

    def is_legal(self):
        # since our operators always generate legal states, we always return True
        return True


"""
Operators
"""


def open_link(state):
    """
    Open every link in chains one by one and return a set of new states
    """
    nstates = []
    links = []
    foundLinks = []
    # find every closed link
    for i in range(state.nchains * 2):
        if i not in foundLinks and state.links[i] != -1:
            foundLinks.append(state.links[i])
            links.append([i, state.links[i]])
    for l, r in links:
        nlinks = list(state.links)
        nlinks[l] = -1
        nlinks[r] = -1
        nstates.append(ChainState(nlinks))
    return nstates


def close_link(state):
    """
    Close every link in chains one by one and return a set of new states
    """
    openLinks = []
    nstates = []
    for i in range(state.nchains * 2):
        if state.links[i] == -1:
            openLinks.append(i)
    linkCombs = itertools.combinations(openLinks, 2)
    for l, r in linkCombs:
        if l // 2 != r // 2:
            nlinks = list(state.links)
            nlinks[l] = r
            nlinks[r] = l
            nstates.append(ChainState(nlinks))
    return nstates


def goal_test(state):
    goal = [23, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15, 18, 17, 20, 19, 22, 21, 0]
    gstate = ChainState(goal)
    return  gstate == state


if __name__ == '__main__':
    initialState = ChainState([-1, 2, 1, 4, 3, -1, -1, 8, 7, 10, 9, -1, -1, 14, 13, 16, 15, -1, -1, 20, 19, 22, 21, -1])
    operators = [
        Operator("Close Link", close_link),
        Operator("Open Link", open_link)
    ]
    problem = SearchProblem(initialState, operators, goal_test)
    node = problem.depth_limited_search(5)
    # node = problem.BreadthFirstSearch()
    for n in problem.get_solution_path(node):
        print(n)