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
8 Puzzle

Created on Feb 6, 2011

@author: goker
"""

from aiama.search import Operator, State, SearchProblem
import random


class EightPuzzleState(State):
    def __init__(self, grid):
        State.__init__(self)
        self.grid = grid

    def __repr__(self):
        return repr(self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def __hash__(self):
        return hash(tuple(self.grid))

    def is_legal(self):
        return True


"""
Operators
"""


def move_blank_left(state):
    blankPos = state.grid.index(0)
    # if blank is not on the left column
    if blankPos % 3 != 0:
        nstate = EightPuzzleState(list(state.grid))
        nstate.grid[blankPos] = nstate.grid[blankPos - 1]
        nstate.grid[blankPos - 1] = 0
        return [nstate]
    return []


def move_blank_right(state):
    blankPos = state.grid.index(0)
    # if blank is not on the right column
    if (blankPos + 1) % 3 != 0:
        nstate = EightPuzzleState(list(state.grid))
        nstate.grid[blankPos] = nstate.grid[blankPos + 1]
        nstate.grid[blankPos + 1] = 0
        return [nstate]
    return []


def move_blank_up(state):
    blankPos = state.grid.index(0)
    # if blank is not on the first row
    if blankPos // 3 != 0:
        nstate = EightPuzzleState(list(state.grid))
        nstate.grid[blankPos] = nstate.grid[blankPos - 3]
        nstate.grid[blankPos - 3] = 0
        return [nstate]
    return []


def move_blank_down(state):
    blankPos = state.grid.index(0)
    # if blank is not on the last row
    if blankPos // 3 != 2:
        nstate = EightPuzzleState(list(state.grid))
        nstate.grid[blankPos] = nstate.grid[blankPos + 3]
        nstate.grid[blankPos + 3] = 0
        return [nstate]
    return []


"""
Goal Test
"""


def eight_puzzle_goal_test(state):
    goalGrid = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if state.grid == goalGrid:
        return True
    return False


def misplaced_tiles_heuristic(state):
    goalGrid = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return sum([1 for i in range(9) if state.grid[i] != goalGrid[i] ])


def manhattan_distance_heuristic(state):
    totDistance = 0
    goalGrid = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    for i in range(3):
        for j in range(3):
            actualIndex = goalGrid.index(state.grid[i*3+j])
            row = actualIndex//3
            col = actualIndex%3
            totDistance = totDistance + abs(i-row) + abs(j-col)
    return totDistance


if __name__ == "__main__":
    initialGrid = list(range(9))
    random.shuffle(initialGrid)
    initialState = EightPuzzleState(initialGrid)

    operators = [
        Operator("Move Blank Left", move_blank_left),
        Operator("Move Blank Right", move_blank_right),
        Operator("Move Blank Up", move_blank_up),
        Operator("Move Blank Down", move_blank_down)
    ]

    problem = SearchProblem(initialState, operators, eight_puzzle_goal_test)

    # node = problem.depth_limited_search(5)
    print('Without heuristic functions')
    node = problem.breadth_first_search()
    for n in problem.get_solution_path(node):
        print(n)
    print()

    problem = SearchProblem(initialState, operators, eight_puzzle_goal_test, None,
                            heuristicFunctions=[misplaced_tiles_heuristic, manhattan_distance_heuristic])

    print('With heuristic functions')
    node = problem.iterative_deepening_a_star_search()
    for n in problem.get_solution_path(node):
        print(n)
