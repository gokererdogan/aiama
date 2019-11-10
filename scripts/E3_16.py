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
Exercise 3.16 - Sequence Prediction
Tests of human intelligence often contain sequence prediction problems. The aim in
such problems is to predict the next member of a sequence of integers, assuming that the number
in position n of the sequence is generated using some sequence function s(n), where the first
element of the sequence corresponds to n = 0. For example, the function s(n) - 2" generates the
sequence [1,2,4,8,16, ...].
In this exercise, you will design a problem-solving system capable of solving such pre-
diction problems. The system will search the space of possible functions until it finds one that
matches the observed sequence. The space of sequence functions that we will consider consists
of all possible expressions built from the elements 1 and n, and the functions +, x, —, /, and
exponentiation. For example, the function 2" becomes (1 + 1)" in this language. It will be useful
to think of function expressions as binary trees, with operators at the internal nodes and 1 's and
«'s at the leaves.
a. First, write the goal test function. Its argument will be a candidate sequence function s. It
will contain the observed sequence of numbers as local state.
b. Now write the successor function. Given a function expression s, it should generate all
expressions one step more complex than s. This can be done by replacing any leaf of the
expression with a two-leaf binary tree.
c. Which of the algorithms discussed in this chapter would be suitable for this problem?
Implement it and use it to find sequence expressions for the sequences [1,2,3,4,5],
[1,2,4,8,16, ...],and [0.5,2,4.5,8].
d. If level d of the search space contains all expressions of complexity d +1, where complexity
is measured by the number of leaf nodes (e.g., n + (1 x n) has complexity 3), prove by
induction that there are roughly 20d(d +1)1 expressions at level d.
e. Comment on the suitability of uninformed search algorithms for solving this problem. Can
you suggest other approaches?

Created on Feb 4, 2011

@author: goker
"""

from aiama.search import Operator, SearchProblem, State


class ExpressionNode:
    """
    Node in a sequence function tree. Has left, right children and value in node
    Value can be 1 or n
    Operators can be +, -, /, *, ^
    """

    def __init__(self, valueOrOp, left=None, right=None):
        self.left = left
        self.right = right
        self.valueOrOp = valueOrOp

    def __repr__(self):
        s = ''
        if self.left is not None:
            s = ("(%s" % (repr(self.left),))
        s = ("%s%s" % (s, self.valueOrOp))
        if self.right is not None:
            s = ("%s%s)" % (s, repr(self.right)))
        return s

    def evaluate(self, n):
        """
        Evaluate expression with given n value
        """
        if self.left is not None and self.right is not None:
            if self.valueOrOp == '+':
                return self.left.evaluate(n) + self.right.evaluate(n)
            elif self.valueOrOp == '-':
                return self.left.evaluate(n) - self.right.evaluate(n)
            elif self.valueOrOp == '*':
                return self.left.evaluate(n) * self.right.evaluate(n)
            elif self.valueOrOp == '/':
                return self.left.evaluate(n) / self.right.evaluate(n)
            elif self.valueOrOp == '^':
                return self.left.evaluate(n) ** self.right.evaluate(n)
        else:
            if self.valueOrOp == 'n':
                return n
            elif self.valueOrOp == 1:
                return 1

    def get_leaves(self):
        if self.left is not None and self.right is not None:
            return [self.left.get_leaves(), self.right.get_leaves()]
        else:
            return self

    def copy(self):
        """
        Copy node. Used in generating new states
        """
        if self.left is not None and self.right is not None:
            return ExpressionNode(self.valueOrOp, self.left.copy(), self.right.copy())
        else:
            return ExpressionNode(self.valueOrOp)

    def update_first_leaf(self, exp, depthLimit, currentDepth):
        """
        Update first found leaf with exp
        """
        if currentDepth > depthLimit:
            return False
        if self.left is not None and self.right is not None:
            if self.left.left is None and self.left.right is None:
                self.left = exp
                return True
            if self.right.left is None and self.right.right is None:
                self.right = exp
                return True
            lOk = self.left.update_first_leaf(exp, depthLimit, currentDepth + 1)
            if not lOk:
                rOk = self.right.update_first_leaf(exp, depthLimit, currentDepth + 1)
                return rOk
            else:
                return True
        return False


class SequenceFunction:
    """
    Tree representing sequence function. Contains root node of type ExpressionNode
    """

    def __init__(self, root):
        self.root = root

    def __repr__(self):
        return repr(self.root)

    def evaluate(self, n):
        try:
            return self.root.evaluate(n)
        except ZeroDivisionError:
            return 1

    def get_leaves(self):
        return self.root.get_leaves()

    def copy(self):
        return SequenceFunction(self.root.copy())

    def update_first_leaf(self, exp):
        """
        Change first leaf found with expression exp
        """
        # if there is only root
        if self.root.left is None and self.root.right is None:
            self.root = exp
            return True
        for i in range(100):
            if self.root.update_first_leaf(exp, i + 1, 0):
                return True
        return False


class SequencePredictionState(State):
    def __init__(self, seqFunction):
        State.__init__(self)
        self.sequenceFunction = seqFunction

    def __repr__(self):
        return repr(self.sequenceFunction)

    def __hash__(self):
        return hash(repr(self.sequenceFunction))

    def is_legal(self):
        return True


def generate_new_state(state):
    ops = '+-*/^'
    vals = [1, 'n']
    nstates = []
    # generate every possible 3-node expression
    for lv in vals:
        for op in ops:
            for rv in vals:
                leftNode = ExpressionNode(lv)
                rightNode = ExpressionNode(rv)
                exp = ExpressionNode(op, leftNode, rightNode)
                # copy sequence function
                nseqFunc = state.sequenceFunction.copy()
                # replace its first leaf with exp
                if nseqFunc.update_first_leaf(exp):
                    nstates.append(SequencePredictionState(nseqFunc))
    return nstates


def goal_test(state):
    seq = [0, 5, 2, 4, 5, 8]
    for n in range(len(seq)):
        if seq[n] != state.sequenceFunction.evaluate(n):
            return False
    return True


if __name__ == '__main__':
    en = ExpressionNode(1)

    seqFunc = SequenceFunction(en)

    initialState = SequencePredictionState(seqFunc)
    operators = [Operator("Add new expression", generate_new_state)]
    problem = SearchProblem(initialState, operators, goal_test)

    # solutionNode = problem.BreadthFirstSearch()
    solutionNode = problem.iterative_deepening_search()
    # print(solutionNode)
    solution = problem.get_solution_path(solutionNode)
    for node in solution:
        print(node)
#
#    
#    ln = ExpressionNode(1)
#    rn = ExpressionNode('n')
#    en = ExpressionNode('/', ln, rn)
#    sf = SequenceFunction(en)
#    print(sf.Evaluate(2))
#    print(seqFunc)
#    print(en.Evaluate(0))
#    print(seqFunc.GetLeaves())
#    nstates = GenerateNewState(initialState)
#    print(nstates)
#    nstates = GenerateNewState(nstates[0])
#    print(nstates)
#    nstates = GenerateNewState(nstates[0])
#    print(nstates)
