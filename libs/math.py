__author__ = 'ktulhy'

from libs.native import *

def math_add_1(bd, ba, overflow, br1, br2):
    """
    mem[bd] += mem[ba]
    overflow = 1 if mem[bd] overflowed else 0
    :param bd: memcell
    :param ba: memcell
    :param overflow: memcell
    :param br1: memcell
    :param br2: memcell
    :return: list(opcode) safe
    """
    ops = \
        asm_set_1(overflow, 0) + \
        asm_repeat_1(ba,
                     asm_add_num_1(ba, -1) +
                     asm_add_num_1(bd, 1) +
                     asm_ifelse_1(bd,
                                  asm_nop(),
                                  asm_add_num_1(overflow, 1),
                                  br1, br2)
                     )

    return ops