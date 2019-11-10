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
Created on Feb 9, 2011

@author: goker
"""

from tkinter import *

from EightPuzzle import *


class EightPuzzleGUI:
    def __init__(self, puzzle, cw, ch, master=None):
        self.frame = Frame(master)
        self.canvasWidth = cw
        self.canvasHeight = ch
        self.puzzle = puzzle
        self.add_button()
        self.add_canvas()
        self.frame.pack()

    def add_button(self):
        self.solveButton = Button(self.frame, width=4, height=2, text="Solve", command=self.solve_puzzle)
        self.solveButton.pack(side=BOTTOM)

    def solve_puzzle(self):
        # solve puzzle
        self.solveButton.config(text="Solving...")
        self.solveButton.pack(side=BOTTOM)
        node = problem.iterative_deepening_a_star_search()
        solution = problem.get_solution_path(node)
        self.solveButton.config(text="Next", command=self.__next)
        self.solveButton.pack(side=BOTTOM)
        solution.reverse()
        solution.pop()
        self.solution = solution

    def __next(self):
        if len(self.solution) != 0:
            self.draw_canvas(self.solution)
        else:
            self.solveButton.config(text="Solved", state="disabled")

    def add_canvas(self):
        self.pcanvas = Canvas(self.frame, width=self.canvasWidth, height=self.canvasHeight)
        self.draw_canvas(None)
        self.pcanvas.pack(side=RIGHT)

    def draw_canvas(self, solution):
        self.hors = 20
        self.vers = 20
        self.w = self.canvasWidth - 2 * self.hors
        self.h = self.canvasHeight - 2 * self.vers

        self.cellWidth = self.w // 3
        self.cellHeight = self.h // 3

        # draw background
        for i in range(4):
            x1 = self.hors
            y1 = self.vers + i * self.cellHeight
            x2 = self.w + self.hors
            y2 = self.vers + i * self.cellHeight
            self.pcanvas.create_line(x1, y1, x2, y2, tags='line')
            x1 = self.hors + i * self.cellWidth
            y1 = self.vers
            x2 = self.hors + i * self.cellWidth
            y2 = self.h + self.vers
            self.pcanvas.create_line(x1, y1, x2, y2, tags='line')

        # draw initial state
        if solution is None:
            self.__drawNumbers(self.puzzle.initialState.grid)
        else:
            node = solution.pop()
            if node is not None:
                self.__drawNumbers(node.state.grid)

    def __drawNumbers(self, grid):
        for i in range(9):
            v = repr(grid[i])
            if v != '0':
                x = (i % 3) * self.cellWidth + self.hors + (self.cellWidth // 2)
                y = (i // 3) * self.cellHeight + self.vers + (self.cellHeight // 2)
                item = self.pcanvas.find_withtag('number' + v)
                if len(item) != 0:
                    xo, yo = tuple(self.pcanvas.coords(item))
                    self.pcanvas.move(item, x - xo, y - yo)
                else:
                    self.pcanvas.create_text(x, y, text=v, tags='number' + v)


def initialize_puzzle():
    initialGrid = list(range(9))
    random.shuffle(initialGrid)
    #    initialGrid = [0, 4, 3, 8, 7, 5, 1, 2, 6]
    initialState = EightPuzzleState(initialGrid)
    operators = [
        Operator("Move Blank Left", move_blank_left),
        Operator("Move Blank Right", move_blank_right),
        Operator("Move Blank Up", move_blank_up),
        Operator("Move Blank Down", move_blank_down)
    ]
    problem = SearchProblem(initialState, operators, eight_puzzle_goal_test, None,
                                   [misplaced_tiles_heuristic, manhattan_distance_heuristic])
    return problem


if __name__ == '__main__':
    problem = initialize_puzzle()
    root = Tk()
    root.title("8 Puzzle")
    app = EightPuzzleGUI(problem, 610, 610, root)
    root.mainloop()