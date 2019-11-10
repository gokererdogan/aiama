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

from TravelingSalesmanProblem import *


class TSPGUI:
    def __init__(self, tsp, cw, ch, master=None):
        self.frame = Frame(master)
        self.canvasWidth = cw
        self.canvasHeight = ch
        self.tsp = tsp
        self.add_button()
        self.add_canvas()
        self.frame.pack()

    def add_button(self):
        self.solveButton = Button(self.frame, width=4, height=2, text="Solve", command=self.solve_tsp)
        self.solveButton.pack(side=BOTTOM)

    def solve_tsp(self):
        # solve tsp
        initialState = TSPState([], 0, [], self.tsp)
        operators = [Operator("Add new edge", generate_new_states)]
        problem = SearchProblem(initialState, operators, goal_test, path_cost, [minimum_spanning_tree_cost])
        # node = problem.UniformCostSearch()
        node = problem.a_star_search()
        self.draw_canvas(node)
        # self.tspcanvas.pack()

    def add_canvas(self):
        self.tspcanvas = Canvas(self.frame, width=self.canvasWidth, height=self.canvasHeight)
        self.draw_canvas(None)
        self.tspcanvas.pack(side=RIGHT)

    def draw_canvas(self, solution):
        hors = 20
        vers = 20
        w = self.canvasWidth - 2 * hors
        h = self.canvasHeight - 2 * vers

        for x, y in self.tsp.locations:
            self.tspcanvas.create_oval(hors + w * x - 3, vers + h * y - 3, hors + w * x + 3, vers + h * y + 3)

        if solution != None:
            for c1, c2 in solution.state.edges:
                self.tspcanvas.create_line(self.tsp.locations[c1][0] * w + hors, self.tsp.locations[c1][1] * h + vers,
                                           self.tsp.locations[c2][0] * w + hors, self.tsp.locations[c2][1] * h + vers)
            startCity = solution.state.edges[len(solution.state.edges) - 1][1]
            endCity = solution.state.edges[0][0]
            self.tspcanvas.create_line(self.tsp.locations[startCity][0] * w + hors,
                                       self.tsp.locations[startCity][1] * h + vers,
                                       self.tsp.locations[endCity][0] * w + hors,
                                       self.tsp.locations[endCity][1] * h + vers)
            pathText = "Total Path Length: %f" % (solution.pathCost)
            self.tspcanvas.create_text(100, 20, text=pathText)


if __name__ == '__main__':
    tsp = TSP(10)
    root = Tk()
    root.title("TSP")
    app = TSPGUI(tsp, 600, 600, root)
    root.mainloop()
