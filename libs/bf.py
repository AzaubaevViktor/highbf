__author__ = 'ktulhy'

from lowlevel_opcode.constants import *


def low_add(x):
    x %= 256
    if x > 128:
        x -= 256
    return [(ADD, x)]

def low_inc():
    return [(ADD, 1)]

def low_dec():
    return [(ADD, -1)]

def low_move(x):
    return [(MOVE, x)]

def low_rel_move(frm, to):
    return [(MOVE, to - frm)]

def low_cycle(opcodes):
    return [(CYCLE_OPEN, -1)] + opcodes + [(CYCLE_CLOSE, -1)]
