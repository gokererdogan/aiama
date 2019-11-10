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
AIMA Chapter 4: Informed Search Methods
4.11 The traveling salesperson problem (TSP) can be solved using the minimum spanning tree
(MST) heuristic, which is used to estimate the cost of completing a tour, given that a partial tour
has already been constructed. The MST cost of a set of cities is the smallest sum of the link costs
of any tree that connects all the cities.
a. Show how this heuristic can be derived using a relaxed version of the TSP.
b. Show that the MST heuristic dominates straight-line distance.
c. Write a problem generator for instances of the TSP where cities are represented by random
points in the unit square.
d. Find an efficient algorithm in the literature for constructing the MST, and use it with an
admissible search algorithm to solve instances of the TSP

Created on Feb 9, 2011

@author: goker
"""
import itertools
import random

from aiama.search import State, Operator, SearchProblem


class TSP:
    """
    Class for representing a euclidean TSP defined by randomly chosen cities in unit square    
    """

    def __init__(self, cityCount):
        self.cityCount = cityCount
        # place each city in a random location
        self.locations = []
        randomGenerator = random.Random()
        for i in range(self.cityCount):
            self.locations.append((randomGenerator.random(), randomGenerator.random()))
        # calculate distances between each city
        self.distances = {}
        cityCombs = itertools.combinations(range(self.cityCount), 2)
        for c1, c2 in cityCombs:
            self.distances[(c1, c2)] = (self.locations[c1][0] - self.locations[c2][0]) ** 2 + (
                        self.locations[c1][1] - self.locations[c2][1]) ** 2
            self.distances[(c2, c1)] = self.distances[(c1, c2)]
        for i in range(self.cityCount):
            self.distances[(i, i)] = 100

    def __repr__(self):
        return "Cities: %s Distances: %s" % (repr(self.locations), repr(self.distances))


class TSPState(State):
    def __init__(self, edges, lastCity, visitedCities, tsp):
        State.__init__(self)
        self.edges = edges
        self.lastCity = lastCity
        self.visitedCities = visitedCities
        self.visitedCities.append(lastCity)
        self.tsp = tsp

    def __repr__(self):
        return repr(self.edges)

    def __hash__(self):
        return hash(tuple(self.edges))

    def is_legal(self):
        # check if we have visited any city twice except starting city
        return True


def generate_new_states(state):
    if len(state.edges) == state.tsp.cityCount - 1:
        return []
    nstates = []
    # generate new states by linking last city to each possible unvisited city including start city 
    for i in range(state.tsp.cityCount):
        if i not in state.visitedCities:
            nedges = list(state.edges)
            nedges.append((state.lastCity, i))
            nstate = TSPState(nedges, i, list(state.visitedCities), state.tsp)
            nstates.append(nstate)
    return nstates


def goal_test(state):
    # have we traveled through all cities
    if len(state.edges) != state.tsp.cityCount - 1:
        return False
    return True


def path_cost(parentState, state):
    # path cost is the distance between last two cities connected
    if len(state.edges) == 0:
        return 0
    return state.tsp.distances[(state.edges[len(state.edges) - 1][0], state.edges[len(state.edges) - 1][1])]


def minimum_spanning_tree_cost(state):
    # construct minimum spanning tree (using Prim's algorithm) for not visited nodes and get its total path cost
    # find the unvisited cities
    vertices = list(range(state.tsp.cityCount))
    [vertices.remove(c) for c in state.visitedCities]
    # mst should contain start and end cities of current path
    vertices.append(state.lastCity)
    if len(state.edges) != 0:
        # add start city
        vertices.append(state.edges[0][0])

    vnew = [vertices[0]]
    enew = []
    while len(vnew) != len(vertices):
        pedges = []
        # for every vertice u in vnew, find edges between this u and v (another vertice not in vnew)
        for u in vnew:
            for v in vertices:
                if v not in vnew:
                    pedges.append((u, v, state.tsp.distances[(u, v)]))
        pedges.sort(key=lambda i: i[2])
        vnew.append(pedges[0][1])
        enew.append(pedges[0])
    totalCost = 0
    for u, v, c in enew:
        totalCost = totalCost + c
    return totalCost


if __name__ == '__main__':
    tsp = TSP(15)
    initialState = TSPState([], 0, [], tsp)
    operators = [Operator("Add new edge", generate_new_states)]
    problem = SearchProblem(initialState, operators, goal_test, path_cost, [minimum_spanning_tree_cost])
    # node = problem.UniformCostSearch()
    node = problem.a_star_search()
    print(node)
