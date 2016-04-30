'''AStar.py
TianYang Jin, Sheng Chen
The problem being formulated is Sliding Blocks of 10 pieces. The pieces consists of four types, 1x1, 2x1, 1x2, and 2x2.
Here is a rough drawing of the Initial state and a representation of the goal state:

1 2 2 7                            . . . .
1 2 2 8                            . . . .
3 5 5 9            ------->        . . . .
3 4 6 10                           . 2 2 .
0 4 6 0                            . 2 2 .

The goal of this game is to get the 2x2 block to the shown position, all other pieces' positions don't matter.
But the piece can only move to an empty space (represented by 0) and it can only move if the space can fit.

In this program, each state of the board is represented by a simple GUI interface produced using the package Tkinter.
It took the ASar search algorithm about 160s to solve the problem using the 'combined_min' heuristic function, and it
displays the solution path at then end using the same simple GUI interface.

CSE 415, Spring 2016, University of Washington
Instructor: S. Tanimoto.
'''

import sys
import queue as Q
import importlib
from tkinter import *
import time

if len(sys.argv) != 4:
    print("Invalid parameter size.\n")
    quit()

try:
    puzzle = sys.argv[1]
    Problem = importlib.import_module(puzzle)
except ImportError:
    quit()

Initial_State = importlib.import_module(sys.argv[3].split('.')[0])

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}
master = Tk()
w = Canvas(master, width=300, height=300)
# colors = {1: 'green', 2: 'red', 3: 'green', 4: 'green', 5: 'blue', 6: 'green', 7: 'wheat', 8: 'wheat', 9: 'wheat',
#           10: 'wheat', 0: 'white'}

def heuristic(s):
    heuristic_function = sys.argv[2]
    if heuristic_function == 'h_blocksInTheWay':
        return Problem.h_blocksInTheWay(s)
    elif heuristic_function == 'h_combined_min':
        return Problem.h_combined_min(s)
    elif heuristic_function == 'h_simple':
        return Problem.h_simple(s)
    elif heuristic_function == 'h_force':
        return Problem.h_force(s)
    else:
        print("Invilid heuristic evaluation function.\n")
        quit()


def runAStar():
    initial_state = Initial_State.CREATE_INITIAL_STATE()
    print("Initial State:")
    Problem.DESCRIBE_STATE(initial_state, w)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterativeAStar(initial_state)
    print(str(COUNT) + " states examined.")


def IterativeAStar(initial_state):
    global COUNT, BACKLINKS

    OPEN = Q.PriorityQueue()
    OPEN.put((heuristic(initial_state), initial_state))
    OPEN_CP = [initial_state]
    CLOSED = []
    BACKLINKS[Problem.HASHCODE(initial_state)] = -1

    while not OPEN.empty():
        (W, S) = OPEN.get()
        g_s = W - heuristic(S)
        # print(Problem.DESCRIBE_STATE(S))
        OPEN_CP.remove(S)
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            # Problem.DESCRIBE_STATE(s, w)
            backtrace(S)
            return

        COUNT += 1
        if (COUNT % 32) == 0:
            print(".", end="")
            if (COUNT % 128) == 0:
                print("COUNT = " + str(COUNT))
                print("len(OPEN)=" + str(OPEN.qsize()))
                print("len(CLOSED)=" + str(len(CLOSED)))
                #print(Problem.DESCRIBE_STATE(S))
        L = []
        for op in Problem.OPERATORS:
            # Optionally uncomment the following when debugging
            # a new problem formulation.
            # print("Trying operator: "+op.name)
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED) and not occurs_in(new_state, OPEN_CP):
                    L.append(new_state)
                    BACKLINKS[Problem.HASHCODE(new_state)] = S
                    # Uncomment for debugging:
                    # print(Problem.DESCRIBE_STATE(new_state))
        for s in L:
            h_s = heuristic(s)
            OPEN.put((g_s + 1 + h_s, s))
        OPEN_CP = OPEN_CP + L


def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[Problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        Problem.DESCRIBE_STATE(s, w)
        time.sleep(0.08)
    print(len(path) - 1)
    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2): return True
    return False


if __name__ == '__main__':
    start_time = time.clock()
    runAStar()
    finish_time = time.clock()
    print('Duration: ' + str(finish_time - start_time))
