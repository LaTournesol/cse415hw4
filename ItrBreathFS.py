'''ItrBreathFS.py
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
import time
from tkinter import *

if sys.argv==[''] or len(sys.argv)<2:
    import SlidingBlocksProblem as Problem
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])


print("\nWelcome to ItrBreathFS")
COUNT = None
BACKLINKS = {}
master = Tk()
w = Canvas(master, width=300, height=300)

def runBFS():
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(Problem.DESCRIBE_STATE(initial_state, w))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterativeBFS(initial_state)
    print(str(COUNT)+" states examined.")

def IterativeBFS(initial_state):
    global COUNT, BACKLINKS

    OPEN = [initial_state]
    CLOSED = []
    BACKLINKS[Problem.HASHCODE(initial_state)] = -1

    while OPEN != []:
        S = OPEN[0]
        del OPEN[0]
        CLOSED.append(S)
        # print(Problem.DESCRIBE_STATE(S))
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            return

        COUNT += 1
        if (COUNT % 32)==0:
            print(".",end="")
            if (COUNT % 128)==0:
                print("COUNT = "+str(COUNT))
                print("len(OPEN)="+str(len(OPEN)))
                print("len(CLOSED)="+str(len(CLOSED)))
        L = []
        for op in Problem.OPERATORS:
            #Optionally uncomment the following when debugging
            #a new problem formulation.
            # print("Trying operator: "+op.name)
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED) and not occurs_in(new_state, OPEN):
                    L.append(new_state)
                    BACKLINKS[Problem.HASHCODE(new_state)] = S
                    #Uncomment for debugging:
                    #print(Problem.DESCRIBE_STATE(new_state))
        rm = []
        for s2 in L:
            for i in range(len(OPEN)):
                if Problem.DEEP_EQUALS(s2, OPEN[i]):
                    del s2; break
        OPEN = OPEN + L

def backtrace(S):
    global BACKLINKS

    path = []
    while not S == -1:
        path.append(S)
        S = BACKLINKS[Problem.HASHCODE(S)]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(Problem.DESCRIBE_STATE(s, w))
        time.sleep(0.08)
    print(len(path))
    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2): return True
    return False

if __name__=='__main__':
    runBFS()