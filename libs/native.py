__author__ = 'ktulhy'

from libs.bf import *

"""Все библиотеки здесь безопасны с точки зрения адресации в памяти.
 Это значит, что они будут правильно работать с mem[0], и после работы MP = 0"""


def asm_set_1(bd, num):
    """
    Устанавливает mem[bd] := num
    :param bd: int
    :param num: int
    :return: list(opcode) safe
    """
    ops = \
        low_rel_move(0, bd) + \
        low_nul() + \
        low_add(num) + \
        low_rel_move(bd, 0)
    return ops


def asm_mov_1(bd, bn):
    """
    mem[bd] := mem[bn]
    mem[bn] := 0
    :param bd: int
    :param bn: int
    :return: list(opcode) safe
    """
    ops = \
        low_rel_move(0, bn) + \
        low_nul() + \
        low_cycle(
            low_block(bn, {
                bn: -1,
                bd: 1
            }, bn)
        ) + \
        low_rel_move(bn, 0)
    return ops


def asm_copy_1(bd, bn, br):
    """
    mem[bd] := mem[bn]
    mem[br] := 0
    :param bd: int
    :param bn: int
    :param br: int
    :return: list(opcode) safe
    """
    ops = \
        asm_set_1(bd, 0) + \
        asm_set_1(br, 0) + \
        low_rel_move(0, bn) + \
        low_cycle(
            low_block(bn, {
                bn: -1,
                br: +1,
                bd: +1
            }, bn)
        ) + \
        low_rel_move(bn, br) + \
        low_cycle(
            low_block(br, {
                br: -1,
                bn: +1
            }, br)
        ) + \
        low_rel_move(br, 0)
    return ops


def asm_cycle_1(cur, opcodes):
    """
    while (mem[cur]) {
        opcodes
    }
    :param cur: int
    :param opcodes: list(opcode), safe
    :return:
    """
    ops = \
        low_rel_move(0, cur) + \
        low_cycle(
            low_rel_move(cur, 0) + \
            opcodes + \
            low_rel_move(0, cur)
        ) + \
        low_rel_move(cur, 0)
