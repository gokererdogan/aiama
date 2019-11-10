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
AIMA Chapter 3: Solving Problems By Searching
Exercise 3.4 
Implement the missionaries and cannibals problem and use breadth-first search to find the
shortest solution. Is it a good idea to check for repeated states? Draw a diagram of the complete
state space to help you decide.
MC is used as an abbreviation for missionaries and cannibals problem
Goker 03.02.2011
"""

from aiama.search import Operator, SearchProblem, State


class MCState(State):
    """
    State representation for missionaries and cannibals problem
    Representation -> Missionary count on left side, Cannibal count on left side
    and boat location(1 if it is on left bank, 0 otherwise)
    """

    def __init__(self, mCount=3, cCount=3, boatLocation=1):
        State.__init__(self)
        self.mCount = mCount
        self.cCount = cCount
        self.boatLocation = boatLocation

    def __eq__(self, other):
        if self.boatLocation == other.boatLocation and self.cCount == other.cCount and self.mCount == other.mCount:
            return True
        return False

    def __repr__(self):
        lb = 'B'
        rb = ''
        if self.boatLocation == 0:
            lb = ''
            rb = 'B'
        return "%dM %dC |%s-%s| %dM %dC" % (self.mCount, self.cCount, lb, rb, 3 - self.mCount, 3 - self.cCount)
        # return "Missionaries on left bank: %d, Cannibals on left bank: %d, Is boat on left bank: %d" % (
        # self.mCount, self.cCount, self.boatLocation)

    def __hash__(self):
        return hash(repr(self.mCount) + repr(self.cCount) + repr(self.boatLocation))

    def is_legal(self):
        cOnRight = 3 - self.cCount
        mOnRight = 3 - self.mCount
        # check if M and C counts are OK
        if 0 <= self.mCount <= 3 and 0 <= self.cCount <= 3:
            if ((self.mCount >= 1 and self.cCount <= self.mCount) or (self.mCount == 0)) and (
                    (mOnRight >= 1 and cOnRight <= mOnRight) or (mOnRight == 0)):
                return True
        return False


"""
Operator functions for MC problem
"""


def move_2m_across(state):
    """
    Move 2 missionaries across the river
    """
    return __move_nm_nc_across(state, 2, 0)


def move_1m_across(state):
    """
    Move 1 missionaries across the river
    """
    return __move_nm_nc_across(state, 1, 0)


def move_2c_across(state):
    """
    Move 2 cannibals across the river
    """
    return __move_nm_nc_across(state, 0, 2)


def move_1c_across(state):
    """
    Move 1 cannibals across the river
    """
    return __move_nm_nc_across(state, 0, 1)


def move_1m1c_across(state):
    """
    Move 1 missionaries 1 cannibals across the river
    """
    return __move_nm_nc_across(state, 1, 1)


def __move_nm_nc_across(state, m, c):
    """
    Generic operator that moves n M and n C across the river
    """
    nboatLocation = 1
    if state.boatLocation == 1:
        c = c * -1
        m = m * -1
        nboatLocation = 0
    return [MCState(state.mCount + m, state.cCount + c, nboatLocation)]


def goal_test(state):
    """
    Goal test function for MC problem
    """
    if state.mCount == 0 and state.cCount == 0 and state.boatLocation == 0:
        return True
    return False


if __name__ == "__main__":
    """
    Problem Definition
    """
    # operators
    operators = [
        Operator("Move 2 M", move_2m_across),
        Operator("Move 1 M", move_1m_across),
        Operator("Move 2 C", move_2c_across),
        Operator("Move 1 C", move_1c_across),
        Operator("Move 1 M 1 C", move_1m1c_across)
    ]

    # create initial state
    initialState = MCState(3, 3, 1)

    # define problem
    MCProblem = SearchProblem(initialState, operators, goal_test)

    node = MCProblem.breadth_first_search()
    solution = MCProblem.get_solution_path(node)
    for n in solution:
        print(n)
