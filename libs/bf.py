__author__ = 'ktulhy'

from lowlevel_opcode.constants import *

""" здесь располагаются небезопасные функции, в начале MP и в конце могут быть разными """


def low_add(x):
    """
    mem[MP] += x
    :param x: int
    :return: list(opcode) absurd safe
    """
    x %= 256
    if x > 128:
        x -= 256
    return [(ADD, x)]

def low_inc():
    """
    mem[MP] += 1
    :return: list(opcode) absurd safe
    """
    return [(ADD, 1)]

def low_dec():
    """
    mem[MP] -= 1
    :return: list(opcode) absurd safe
    """
    return [(ADD, -1)]

def low_move(x):
    """
    MP += x
    :param x: int
    :return: list(opcode) UNSAFE
    """
    return [(MOVE, x)]

def low_rel_move(frm, to):
    """
    MP == frm -> MP := to
    :param frm: memcell, текущее положение MP
    :param to: memcell, нужное положение MP
    :return: list(opcode) UNSAFE
    """
    return low_move(to - frm)

def low_block(cur, changes, end):
    """
    Находясь в cur, применяет изменения, описаные в changes, и под конец работы оказывается в end
    :param cur: memcell
    :param changes: dict(int:int)
    :param end: memcell
    :return: list(opcode) UNSAFE
    """
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
    """
    Небезопасный цикл, раскрывается в [ opcodes ]
    :param opcodes: list(opcode) unsafe
    :return: list(opcode) UNSAFE
    """
    return [(CYCLE_OPEN, -1)] + opcodes + [(CYCLE_CLOSE, -1)]

def low_nul():
    """
    mem[MP] := 0
    :return: list(opcode) absurd safe
    """
    return low_cycle(low_dec())

def low_nop():
    """
    Ничего не делает
    :return: list(opcode) safe
    """
    return [(NOP, )]
