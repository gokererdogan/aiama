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
E3.20a - Cryptarithmetic Problem

FORTY
  TEN
  TEN
+
-----
SIXTY
Created on Feb 7, 2011

@author: goker
"""

from aiama.search import CSP


def check_constraints(state):
    assignments = dict(state.assignments)
    # find unassigned variables
    unassignedVars = list(state.varList)
    [unassignedVars.remove(k) for k in state.assignments.keys()]
    for v in unassignedVars:
        assignments[v] = -1

    vals = list(state.assignments.values())
    for i in range(10):
        if vals.count(i) > 1:
            return False

            # F and S cannot be 0
    if assignments['F'] == 0 or assignments['S'] == 0:
        return False
    if assignments['Y'] != -1 and assignments['N'] != -1:
        # check every step of summation
        firstCarry = (assignments['Y'] + 2 * assignments['N']) // 10
        if (assignments['Y'] + 2 * assignments['N']) % 10 != assignments['Y']:
            return False

        if assignments['T'] != -1 and assignments['E'] != -1:
            secondCarry = (assignments['T'] + 2 * assignments['E'] + firstCarry) // 10
            if (assignments['T'] + 2 * assignments['E'] + firstCarry) % 10 != assignments['T']:
                return False

            if assignments['R'] != -1 and assignments['T'] != -1 and assignments['X'] != -1:
                thirdCarry = (assignments['R'] + 2 * assignments['T'] + secondCarry) // 10
                if (assignments['R'] + 2 * assignments['T'] + secondCarry) % 10 != assignments['X']:
                    return False

                if assignments['O'] != -1 and assignments['I'] != -1:
                    fourthCarry = (assignments['O'] + thirdCarry) // 10
                    if (assignments['O'] + thirdCarry) % 10 != assignments['I']:
                        return False

                    if assignments['F'] != -1 and assignments['S'] != -1:
                        if (assignments['F'] + fourthCarry) != assignments['S']:
                            return False

    return True


if __name__ == '__main__':
    varsAndDomains = {('Y', 'N', 'T', 'E', 'R', 'O', 'F', 'S', 'I', 'X'): [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
    csp = CSP(varsAndDomains, [check_constraints])
    solution = csp.solve()
    print(solution)
