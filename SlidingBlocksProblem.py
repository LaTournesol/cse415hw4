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

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Basic Eight Puzzle"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['TianYang Jin']
PROBLEM_CREATION_DATE = "18-APR-2016"
PROBLEM_DESC = \
    '''This formulation of the Basic Eight Puzzle problem uses generic
    Python 3 constructs and has been tested with Python 3.4.
    It is designed to work according to the QUIET tools interface.
    '''
# </METADATA>

# <COMMON_CODE>
TYPES = {1: "2x1", 2: "2x2", 3: "2x1", 4: "2x1", 5: "1x2", 6: "2x1", 7: "1x1", 8: "1x1", 9: "1x1", 10: "1x1"}


def DEEP_EQUALS(s1, s2):
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


# def can_move(s, From, To):
#     '''Tests whether it's legal to move a disk in state s
#        from the From peg to the To peg.'''
#     try:
#         first = s[From[0]]
#         for i in From:
#             if s[i] != first:
#                 return False
#         X = []
#         for item in To:
#             if item not in From:
#                 X.append(item)
#         for x in X:
#             if s[x] != 0:
#                 return False
#         return True
#     except (Exception) as e:
#         print(e)


def can_move(s, From, To):
    try:
        type = TYPES[s[From[0]]]
    except KeyError:
        return False

    if type == '1x1':
        if len(From) != 1:
            return False
        else:
            if s[To[0]] == 0:
                return True
            else:
                return False
    elif type == '1x2':
        if len(From) != 2 or not (s[From[0]] == s[From[1]]):
            return False
        if From[1] - From[0] != 1:
            return False
        I = []
        for i in To:
            if i not in From:
                I.append(i)
        for i in I:
            if s[i] != 0:
                return False
        return True
    elif type == '2x1':
        if len(From) != 2 or not (s[From[0]] == s[From[1]]):
            return False
        if From[1] - From[0] != C_size:
            return False
        I = []
        for i in To:
            if i not in From:
                I.append(i)
        for i in I:
            if s[i] != 0:
                return False
        return True
    else:
        if len(From) != 4 or not (s[From[0]] == s[From[1]] == s[From[2]] == s[From[3]]):
            return False
        I = []
        for i in To:
            if i not in From:
                I.append(i)
        for i in I:
            if s[i] != 0:
                return False
        return True


def move(s, From, To):
    news = copy_state(s)  # start with a deep copy.
    type = s[From[0]]
    for i in To:
        if i not in From:
            news[i] = type
    for j in From:
        if j not in To:
            news[j] = 0
    return news  # return new state

def to_2d(i):
    x = i % C_size
    y = i // C_size
    return x, y


def h_blocksInTheWay(s):
    lc = s.index(2)
    types = []
    n = 0
    if lc % 4 == 0:
        types.insert(s[lc + 2], s[lc + 6])
        lc += 1
    elif lc % 4 == 2:
        types.insert(s[lc - 1], s[lc + 3])
        lc -= 1
    for o in [8, 12, 16, 9, 13, 17]:
        if 0 <= lc + o <= 19:
            types.append(s[lc + o])
    unique_types = set(types)
    n = len(unique_types)
    if 0 in unique_types: n -= 1
    return n

def get_min_d(c, b):
    # smallest distance from 1x1 blocks to 2x2 blocks
    xc, yc = to_2d(c)
    xc2 = xc + 1
    xc3 = xc
    xc4 = xc + 1
    yc2 = yc
    yc3 = yc + 1
    yc4 = yc + 1
    xb, yb = to_2d(b)
    min = abs(xb-xc) + abs(yb-yc)
    for (x, y) in [(xc2, yc2), (xc3, yc3), (xc4, yc4)]:
        if abs(xb-x) + abs(yb-y) < min:
            min = abs(xb-x) + abs(yb-y)
    return min


def h_combined_min(s):
    xc, yc = to_2d(s.index(2))
    d = abs(4 - yc) - 1
    d += get_min_d(s.index(2), s.index(7))
    d += get_min_d(s.index(2), s.index(8))
    d += get_min_d(s.index(2), s.index(9))
    d += get_min_d(s.index(2), s.index(10))
    return d


def h_simple(s):
    xc, yc = to_2d(s.index(2))
    d = abs(1 - xc) + abs(4 - yc) - 1
    return d


def h_force(s):
    xc = s.index(2)
    if xc == 1: return 3
    if xc == 0 or xc == 2: return 3.5
    if xc == 5: return 2
    if xc == 4 or xc == 6: return 2.5
    if xc == 9: return 1
    if xc == 8 or xc == 10: return 1.5
    if xc == 12 or xc == 14: return 0.5
    if xc == 13: return 0


def h_smallBlocksCloser(s):
    xc, yc = to_2d(s.index(2))       # location of left upper left corner of the Cao's  block
    xg, yg = 1, 4                    # location of the left block of the goal block
    d = abs(xg - xc) + abs(yg - yc) - 1



def goal_test(s):
    '''If the first two pegs are empty, then s is a goal state.'''
    return s[13] == s[14] == s[17] == s[18] == 2


def goal_message(s):
    return "General Cao is out!!"


def get_2d_coord(index):
    x = index % N_size
    y = index // N_size
    return (x, y)


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <COMMON_DATA>
R_size = 5
C_size = 4
# </COMMON_DATA>

# <INITIAL_STATE>
# example initial states
# CREATE_INITIAL_STATE = lambda: [1, 2, 2, 3, 1, 2, 2, 3, 4, 5, 5, 6, 4, 7, 8, 6, 9, 0, 0, 10]
CREATE_INITIAL_STATE = lambda : [0, 5, 5, 3, 1, 7, 8, 3, 1, 2, 2, 6, 4, 2, 2, 6, 4, 9, 10, 0]
#CREATE_INITIAL_STATE = lambda: [1, 5, 5, 3, 1, 7, 8, 3, 4, 2, 2, 6, 4, 2, 2, 6, 0, 9, 10, 0]
# CREATE_INITIAL_STATE = lambda : [3, 1, 2, 4, 0, 5, 6, 7, 8]
# CREATE_INITIAL_STATE = lambda : [1, 4, 2, 3, 7, 0, 6, 8, 5]



DUMMY_STATE = [0, 0, 0, 0, 0, 0, 0, 0, 0]
# </INITIAL_STATE>

# <OPERATORS>

possible_moves = [((0,), (4,)), ((0,), (1,)), ((1,), (5,)), ((1,), (0,)), ((1,), (2,)), ((2,), (6,)), ((2,), (1,)),
                  ((2,), (3,)), ((3,), (7,)), ((3,), (2,)), ((4,), (0,)), ((4,), (8,)), ((4,), (5,)), ((5,), (1,)),
                  ((5,), (9,)), ((5,), (4,)), ((5,), (6,)), ((6,), (2,)), ((6,), (10,)), ((6,), (5,)), ((6,), (7,)),
                  ((7,), (3,)), ((7,), (11,)), ((7,), (6,)), ((8,), (4,)), ((8,), (12,)), ((8,), (9,)), ((9,), (5,)),
                  ((9,), (13,)), ((9,), (8,)), ((9,), (10,)), ((10,), (6,)), ((10,), (14,)), ((10,), (9,)),
                  ((10,), (11,)), ((11,), (7,)), ((11,), (15,)), ((11,), (10,)), ((12,), (8,)), ((12,), (16,)),
                  ((12,), (13,)), ((13,), (9,)), ((13,), (17,)), ((13,), (12,)), ((13,), (14,)), ((14,), (10,)),
                  ((14,), (18,)), ((14,), (13,)), ((14,), (15,)), ((15,), (11,)), ((15,), (19,)), ((15,), (14,)),
                  ((16,), (12,)), ((16,), (17,)), ((17,), (13,)), ((17,), (16,)), ((17,), (18,)), ((18,), (14,)),
                  ((18,), (17,)), ((18,), (19,)), ((19,), (15,)), ((19,), (18,)),
                  ((0, 4), (4, 8)), ((0, 4), (1, 5)), ((1, 5), (5, 9)), ((1, 5), (0, 4)), ((1, 5), (2, 6)),
                  ((2, 6), (6, 10)), ((2, 6), (1, 5)), ((2, 6), (3, 7)), ((3, 7), (7, 11)), ((3, 7), (2, 6)),
                  ((4, 8), (0, 4)), ((4, 8), (8, 12)), ((4, 8), (5, 9)), ((5, 9), (1, 5)), ((5, 9), (9, 13)),
                  ((5, 9), (4, 8)), ((5, 9), (6, 10)), ((6, 10), (2, 6)), ((6, 10), (10, 14)), ((6, 10), (5, 9)),
                  ((6, 10), (7, 11)), ((7, 11), (3, 7)), ((7, 11), (11, 15)), ((7, 11), (6, 10)), ((8, 12), (4, 8)),
                  ((8, 12), (12, 16)), ((8, 12), (9, 13)), ((9, 13), (5, 9)), ((9, 13), (13, 17)), ((9, 13), (8, 12)),
                  ((9, 13), (10, 14)), ((10, 14), (6, 10)), ((10, 14), (14, 18)), ((10, 14), (9, 13)),
                  ((10, 14), (11, 15)), ((11, 15), (7, 11)), ((11, 15), (15, 19)), ((11, 15), (10, 14)),
                  ((12, 16), (8, 12)), ((12, 16), (13, 17)), ((13, 17), (9, 13)), ((13, 17), (12, 16)),
                  ((13, 17), (14, 18)), ((14, 18), (10, 14)), ((14, 18), (13, 17)), ((14, 18), (15, 19)),
                  ((15, 19), (11, 15)), ((15, 19), (14, 18)),
                  ((0, 1), (4, 5)), ((0, 1), (1, 2)), ((1, 2), (5, 6)), ((1, 2), (0, 1)), ((1, 2), (2, 3)),
                  ((2, 3), (6, 7)), ((2, 3), (1, 2)), ((4, 5), (0, 1)), ((4, 5), (8, 9)), ((4, 5), (5, 6)),
                  ((5, 6), (1, 2)), ((5, 6), (9, 10)), ((5, 6), (4, 5)), ((5, 6), (6, 7)), ((6, 7), (2, 3)),
                  ((6, 7), (10, 11)), ((6, 7), (5, 6)), ((8, 9), (4, 5)), ((8, 9), (12, 13)), ((8, 9), (9, 10)),
                  ((9, 10), (5, 6)), ((9, 10), (13, 14)), ((9, 10), (8, 9)), ((9, 10), (10, 11)), ((10, 11), (6, 7)),
                  ((10, 11), (14, 15)), ((10, 11), (9, 10)), ((12, 13), (8, 9)), ((12, 13), (16, 17)),
                  ((12, 13), (13, 14)), ((13, 14), (9, 10)), ((13, 14), (17, 18)), ((13, 14), (12, 13)),
                  ((13, 14), (14, 15)), ((14, 15), (10, 11)), ((14, 15), (18, 19)), ((14, 15), (13, 14)),
                  ((16, 17), (12, 13)), ((16, 17), (17, 18)), ((17, 18), (13, 14)), ((17, 18), (16, 17)),
                  ((17, 18), (18, 19)), ((18, 19), (14, 15)), ((18, 19), (17, 18)),
                  ((0, 1, 4, 5), (1, 2, 5, 6)), ((0, 1, 4, 5), (4, 5, 8, 9)), ((1, 2, 5, 6), (2, 3, 6, 7)),
                  ((1, 2, 5, 6), (5, 6, 9, 10)), ((1, 2, 5, 6), (0, 1, 4, 5)), ((2, 3, 6, 7), (1, 2, 5, 6)),
                  ((2, 3, 6, 7), (6, 7, 10, 11)), ((4, 5, 8, 9), (0, 1, 4, 5)), ((4, 5, 8, 9), (5, 6, 9, 10)),
                  ((4, 5, 8, 9), (8, 9, 12, 13)), ((5, 6, 9, 10), (4, 5, 8, 9)), ((5, 6, 9, 10), (1, 2, 5, 6)),
                  ((5, 6, 9, 10), (6, 7, 10, 11)), ((5, 6, 9, 10), (9, 10, 13, 14)), ((6, 7, 10, 11), (5, 6, 9, 10)),
                  ((6, 7, 10, 11), (2, 3, 6, 7)), ((6, 7, 10, 11), (10, 11, 14, 15)), ((8, 9, 12, 13), (4, 5, 8, 9)),
                  ((8, 9, 12, 13), (9, 10, 13, 14)), ((8, 9, 12, 13), (12, 13, 16, 17)),
                  ((9, 10, 13, 14), (8, 9, 12, 13)),
                  ((9, 10, 13, 14), (5, 6, 9, 10)), ((9, 10, 13, 14), (10, 11, 14, 15)),
                  ((9, 10, 13, 14), (13, 14, 17, 18)),
                  ((10, 11, 14, 15), (9, 10, 13, 14)), ((10, 11, 14, 15), (6, 7, 10, 11)),
                  ((10, 11, 14, 15), (14, 15, 18, 19)),
                  ((12, 13, 16, 17), (8, 9, 12, 13)), ((12, 13, 16, 17), (13, 14, 17, 18)),
                  ((13, 14, 17, 18), (12, 13, 16, 17)),
                  ((13, 14, 17, 18), (9, 10, 13, 14)), ((13, 14, 17, 18), (14, 15, 18, 19)),
                  ((14, 15, 18, 19), (13, 14, 17, 18)),
                  ((14, 15, 18, 19), (10, 11, 14, 15)), ((0, 1), (4, 5)), ((0, 1), (1, 2)), ((1, 2), (0, 1)),
                  ((1, 2), (5, 6)), ((1, 2), (2, 3)), ((2, 3), (6, 7))]
OPERATORS = [Operator("Move number from " + str(p) + " to " + str(q),
                      lambda s, p=p, q=q: can_move(s, p, q),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, p=p, q=q: move(s, p, q))
             for (p, q) in possible_moves]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

# <STATE_VIS>
if 'BRYTHON' in globals():
    from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
    from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
# if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
# </STATE_VIS>
