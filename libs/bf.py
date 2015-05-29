__author__ = 'ktulhy'

from lowlevel_opcode.constants import *

""" здесь располагаются небезопасные функции, в начале MP и в конце могут быть разными """


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
    return low_move(to - frm)

def low_block(cur, changes, end):
    # may optimise
    keys = list(changes.keys())
    keys.sort()
    ops = []
    ops += low_rel_move(cur, keys[0])
    prev_key = keys[0]

    for key in keys:
        ops += low_rel_move(prev_key, key)
        ops += low_add(changes[key])
        prev_key = key

    ops += low_rel_move(keys[-1], end)
    return ops

def low_cycle(opcodes):
    return [(CYCLE_OPEN, -1)] + opcodes + [(CYCLE_CLOSE, -1)]

def low_nul():
    return low_cycle(low_dec())
