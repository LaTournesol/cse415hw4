'''EightPuzzleWithHeuristics.py
TianYang Jin
CSE 415, Spring 2016, University of Washington
Instructor: S. Tanimoto.
Assignment 3 Part II. Eight Puzzle with 4 different heuristics functions

A QUIET Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this
problem formulation.

CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''

import math

#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['TianYang Jin']
PROBLEM_CREATION_DATE = "18-APR-2016"
PROBLEM_DESC= \
    '''This formulation of the Basic Eight Puzzle problem uses generic
    Python 3 constructs and has been tested with Python 3.4.
    It is designed to work according to the QUIET tools interface.
    '''
#</METADATA>

#<COMMON_CODE>
TYPIES = ['1x2', '2x1', '2x2', '1x1']
def DEEP_EQUALS(s1,s2):
    for i in range(0, len(s1)):
        if s1[i] != s2[i]:
            return False
    return True

def DESCRIBE_STATE(state):
    # Produces a textual description of a state.
    # Might not be needed in normal operation with GUIs.
    s = ''
    for i in range(R_size):
        for j in range(C_size):
            s += str(state[C_size * i + j]) + ' '
        s += '\n'
    return s

def HASHCODE(s):
    '''The result should be an immutable object such as a string
    that is unique for the state s.'''
    result = ''
    for i in s:
        result += str(i) + ';'
    return result

def copy_state(s):
    # Performs an appropriately deep copy of a state,
    # for use by operators in creating new states.
    news = s[:]
    return news



def can_move(s,From,To):
    '''Tests whether it's legal to move a disk in state s
       from the From peg to the To peg.'''
    try:
        if (From < 0) or (From >= N_size * N_size) or (To < 0) or (To >= N_size * N_size): return False   # Illegal indices
        if s[From] == 0: return False   # Cannot move from an empty space
        if s[To] != 0: return False     # Cannot move to a non empty space
        return True
    except (Exception) as e:
        print(e)

def move(s,From,To):
    '''Assuming it's legal to make the move, this computes
       the new state resulting from moving the topmost disk
       from the From peg to the To peg.'''
    news = copy_state(s) # start with a deep copy.
    news[To] = s[From]
    news[From] = 0
    return news # return new state

def goal_test(s):
    '''If the first two pegs are empty, then s is a goal state.'''
    return s == [0, 1, 2, 3, 4, 5, 6, 7, 8]


def goal_message(s):
    return "The Eight Puzzle is complete!"

goal_s = [0, 1, 2, 3, 4, 5, 6, 7, 8]
def h_euclidean(s):
    '''Return the euclidean distance between current state and goal state'''
    d = 0
    for i in range(0, len(s)):
        d += (s[i] - goal_s[i]) ** 2
    return math.sqrt(d)


def h_hamming(s):
    '''Return ith number of tiles that, in state s, are not where they should end up in the goal state.'''
    n = 0
    for i in range(0, len(s)):
        if s[i] != goal_s[i]:
            n += 1
    return n

def h_manhattan(s):
    '''Return the 1 norm distance between current state and the goal state'''
    d = 0
    for e in goal_s:
        (x1, y1) = get_2d_coord(e)
        (x2, y2) = get_2d_coord(s.index(e))
        d += abs(x2 - x1) + abs(y2 - y1)
    return d

def get_2d_coord(index):
    x = index % N_size
    y = index // N_size
    return (x, y)


def h_custom(s):
    '''Return the largest absolute distance of all'''
    d = 0
    for i in range(len(s)):
        if abs(s[i]-goal_s[i]) > d:
            d = abs(s[i]-goal_s[i])
    return d

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)

#</COMMON_CODE>

#<COMMON_DATA>
R_size = 5
C_size = 4
#</COMMON_DATA>

#<INITIAL_STATE>
#example initial states
CREATE_INITIAL_STATE = lambda: [0, 1, 2, 3, 4, 5, 6, 7, 8]
#CREATE_INITIAL_STATE = lambda : [1, 0, 2, 3, 4, 5, 6, 7, 8]
#CREATE_INITIAL_STATE = lambda : [3, 1, 2, 4, 0, 5, 6, 7, 8]
#CREATE_INITIAL_STATE = lambda : [1, 4, 2, 3, 7, 0, 6, 8, 5]



DUMMY_STATE = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#</INITIAL_STATE>

#<OPERATORS>

possible_moves = {'2x2':[((0, 1, 4, 5), (1, 2, 5, 6)), ((0, 1, 4, 5), (4, 5, 8, 9)), ((1, 2, 5, 6), (2, 3, 6, 7)),
                         ((1, 2, 5, 6), (5, 6, 9, 10)), ((1, 2, 5, 6), (0, 1, 4, 5)), ((2, 3, 6, 7), (1, 2, 5, 6)),
                         ((2, 3, 6, 7), (6, 7, 10, 11)), ((4, 5, 8, 9), (0, 1, 4, 5)), ((4, 5, 8, 9), (5, 6, 9, 10)),
                         ((4, 5, 8, 9), (8, 9, 12, 13)), ((5, 6, 9, 10), (4, 5, 8, 9)), ((5, 6, 9, 10), (1, 2, 5, 6)),
                         ((5, 6, 9, 10), (6, 7, 10, 11)), ((5, 6, 9, 10), (9, 10, 13, 14)), ((6, 7, 10, 11), (5, 6, 9, 10)),
                         ((6, 7, 10, 11), (2, 3, 6, 7)), ((6, 7, 10, 11), (10, 11, 14, 15)), ((8, 9, 12, 13), (4, 5, 8, 9)),
                         ((8, 9, 12, 13), (9, 10, 13, 14)), ((8, 9, 12, 13), (12, 13, 16, 17)), ((9, 10, 13, 14), (8, 9, 12, 13)),
                         ((9, 10, 13, 14), (5, 6, 9, 10)), ((9, 10, 13, 14), (10, 11, 14, 15)), ((9, 10, 13, 14), (13, 14, 17, 18)),
                         ((10, 11, 14, 15), (9, 10, 13, 14)), ((10, 11, 14, 15), (6, 7, 10, 11)), ((10, 11, 14, 15), (14, 15, 18, 19)),
                         ((12, 13, 16, 17), (8, 9, 12, 13)), ((12, 13, 16, 17), (13, 14, 17, 18)), ((13, 14, 17, 18), (12, 13, 16, 17)),
                         ((13, 14, 17, 18), (9, 10, 13, 14)), ((13, 14, 17, 18), (14, 15, 18, 19)), ((14, 15, 18, 19), (13, 14, 17, 18)),
                         ((14, 15, 18, 19), (10, 11, 14, 15))],
                  '1x2':[((0,1),(4,5)),((0,1),(1,2)),((1,2),(0,1)),((1,2),(5,6)),((1,2),(2,3)),((2,3),(6,7)),
                         ((2,3),(1,2)),((4,5),(0,1)),((4,5),(5,6)),((4,5),(8,9)),((5,6),(4,5)),((5,6),(1,2)),
                         ((5,6),(6,7)),((5,6),(9,10)),((6,7),(2,3)),((6,7),(5,6)),((6,7),(10,11)),((8,9),(4,5)),
                         ((8,9),(9,10)),((8,9),(12,13)),((9,10),(5,6)),((9,10),(8,9)),((9,10),(10,11)),((9,10),(13,14)),
                         ((10,11),(6,7)),((10,11),(9,10)),((10,11),(14,15)),((12,13),(8,9)),((12,13),(13,14)),
                         ((13,14),(9,10)),((13,14),(12,13)),((13,14),(14,15))],
                  '2x1':[((0,4),(1,5)),((0,4),(4,8)),((1,5),(0,4)),((1,5),(2,6)),((1,5),(5,9)),((2,6),(1,5)),
                         ((2,6),(3,7)),((2,6),(6,10)),((3,7),(2,6)),((3,7),(7,11)),((4,8),(0,4)),((4,8),(5,9)),
                         ((4,8),(8,12)),((5,9),(4,8)),((5,9),(1,5)),((5,9),(6,10)),((5,9),(9,13)),((6,10),(2,6)),
                        ((6,10),(5,9)),((6,10),(7,11)),((6,10),(10,14)),((7,11),(3,7)),((7,11),(6,10)),((7,11),(11,15)),
                         ((8, 12,),(9,13)),((8,12),(4,8)),((8,12),(12,16)),((9,13),(5,9)),((9,13),(8,12)),((9,13),(10,14))],
                  '1x1':[(0, 4), (0, 1), (1, 5), (1, 0), (1, 2), (2, 6), (2, 1), (2, 3), (3, 7), (3, 2), (3, 4), (4, 0),
                         (4, 8), (4, 3), (4, 5), (5, 1), (5, 9), (5, 4), (5, 6), (6, 2), (6, 10), (6, 5), (6, 7), (7, 3),
                         (7, 11), (7, 6), (7, 8), (8, 4), (8, 12), (8, 7), (8, 9), (9, 5), (9, 13), (9, 8), (9, 10),
                         (10, 6), (10, 14), (10, 9), (10, 11), (11, 7), (11, 15), (11, 10), (11, 12), (12, 8), (12, 16),
                         (12, 11), (12, 13), (13, 9), (13, 17), (13, 12), (13, 14), (14, 10), (14, 18), (14, 13),
                         (14, 15), (15, 11), (15, 19), (15, 14), (15, 16), (16, 12), (16, 15), (16, 17), (17, 13),
                         (17, 16), (17, 18), (18, 14), (18, 17), (18, 19), (19, 15), (19, 18)]}
OPERATORS = [Operator("Move number from "+str(p)+" to "+str(q),
                      lambda s,p=p,q=q: can_move(s,p,q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s,p=p,q=q: move(s,p,q) )
             for (p,q) in possible_moves]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if 'BRYTHON' in globals():
    from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
    from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
#</STATE_VIS>
