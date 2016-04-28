''' AStar.py Changed 
TianYang Jin
CSE 415, Spring 2016, University of Washington
Instructor: S. Tanimoto.
Assignment 3 Part II. AStar Search

'''

import sys
import queue as Q
import importlib

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

def heuristic(s):
    heuristic_function = sys.argv[2]
    if heuristic_function == 'h_euclidean':
        return Problem.h_euclidean(s)
    elif heuristic_function == 'h_hamming':
        return Problem.h_hamming(s)
    elif heuristic_function == 'h_manhattan':
        return Problem.h_manhattan(s)
    elif heuristic_function == 'h_custom':
        return Problem.h_custom(s)
    else:
        print("Invilid heuristic evaluation function.\n")
        quit()

def runAStar():
    initial_state = Initial_State.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(Problem.DESCRIBE_STATE(initial_state))
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    IterativeAStar(initial_state)
    print(str(COUNT)+" states examined.")

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
        OPEN_CP.remove(S)
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            return
        COUNT += 1
        if (COUNT % 32)==0:
            print(".",end="")
            if (COUNT % 128)==0:
                print("COUNT = "+str(COUNT))
                print("len(OPEN)="+str(OPEN.qsize()))
                print("len(CLOSED)="+str(len(CLOSED)))
        L = []
        for op in Problem.OPERATORS:
            #Optionally uncomment the following when debugging
            #a new problem formulation.
            # print("Trying operator: "+op.name)
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED) and not occurs_in(new_state, OPEN_CP):
                    L.append(new_state)
                    BACKLINKS[Problem.HASHCODE(new_state)] = S
                    #Uncomment for debugging:
                    # print(Problem.DESCRIBE_STATE(new_state))
        # rm = []
        # for s2 in L:
        #     for i in range(len(OPEN_CP)):
        #         if Problem.DEEP_EQUALS(s2, OPEN_CP[i]):
        #             rm = s2; break
        #
        # if len(rm) != 0:
        #     L.remove(rm)
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
        print(Problem.DESCRIBE_STATE(s))
    print(len(path)-1)
    return path


def occurs_in(s1, lst):
    for s2 in lst:
        if Problem.DEEP_EQUALS(s1, s2): return True
    return False

if __name__=='__main__':
    runAStar()

