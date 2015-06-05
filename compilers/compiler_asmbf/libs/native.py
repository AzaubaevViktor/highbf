__author__ = 'ktulhy'

from compilers.compiler_asmbf.libs.bf import *

"""Все библиотеки здесь безопасны с точки зрения адресации в памяти.
 Это значит, что они будут правильно работать с mem[0], и после работы MP = 0"""


def asm_add_num_1(bd, num):
    """
    mem[bd] += num
    :param bd: memcell
    :param num: int
    :return: list(opcode) safe
    """
    ops = \
        low_rel_move(0, bd) + \
        low_add(num) + \
        low_rel_move(bd, 0)
    return ops


def asm_set_1(bd, num):
    """
    mem[bd] := num
    :param bd: memcell
    :param num: int
    :return: list(opcode) safe
    """
    ops = \
        low_rel_move(0, bd) + \
        low_nul() + \
        low_rel_move(bd, 0) + \
        asm_add_num_1(bd, num)
    return ops


def asm_add_mul_destroyable_1(bd, bn, multiplier):
    """
    mem[bd] += mem[bn] * multiplier
    mem[bn] := 0
    :param bd: memcell
    :param bn: memcell
    :param multiplier: int
    :return: list(opcode) safe
    """
    ops = \
        low_rel_move(0, bn) + \
        low_cycle(
            low_block(bn, {
                bn: -1,
                bd: +multiplier
            }, bn)
        ) + \
        low_rel_move(bn, 0)
    return ops


def asm_mov_mul_destroyable_1(bd, bn, multiplier):
    """
    mem[bd] := mem[bn] * multiplier
    mem[bn] := 0
    :param bd: memcell
    :param bn: memcell
    :param multiplier: int
    :return: list(opcode) safe
    """
    ops = \
        asm_set_1(bd, 0) + \
        asm_add_mul_destroyable_1(bd, bn, multiplier)
    return ops


def asm_add_mul_1(bd, bn, multiplier, br):
    """
    mem[bd] += mem[bn] * multiplier
    mem[bn] == mem[bn]
    mem[br] := 0
    :param bd: memcell
    :param bn: memcell
    :param multiplier: int
    :param br: memcell
    :return: list(opcode) safe
    """
    ops = \
        asm_set_1(br, 0) + \
        low_rel_move(0, bn) + \
        low_cycle(
            low_block(bn, {
                bn: -1,
                br: +1,
                bd: +multiplier
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


def asm_mov_mul_1(bd, bn, multiplier, br):
    """
    mem[bd] := mem[bn] * multiplier
    mem[nb] == mem[bn]
    mem[br] := 0
    :param bd: memcell
    :param bn: memcell
    :param multiplier: int
    :param br: memcell
    :return: list(opcode) safe
    """

    ops = \
        asm_set_1(bd, 0) + \
        asm_add_mul_1(bd, bn, multiplier, br)
    return ops


def asm_cycle_1(cur, opcodes):
    """
    while (mem[cur]) {
        opcodes
    }
    :param cur: memcell
    :param opcodes: list(opcode), safe
    :return:
    """
    ops = \
        low_rel_move(0, cur) + \
        low_cycle(
            low_rel_move(cur, 0) +
            opcodes +
            low_rel_move(0, cur)
        ) + \
        low_rel_move(cur, 0)
    return ops


def asm_repeat_1(cur, opcodes):
    """
    while (mem[cur] != 0) {
        mem[cur] -= 1
        opcodes
    }
    :param cur: memcell
    :param opcodes: list(opcode) safe
    :return: list(opcode) safe
    """
    ops = \
        asm_cycle_1(cur,
                    asm_add_num_1(cur, -1) +
                    opcodes)
    return ops


def asm_ifelse_1(cur, opcodes_true, opcodes_false, br1, br2):
    """
    if (mem[cur]) {
        opcodes
    }
    mem[br1] := 0
    mem[br2] := 0
    :param cur: memcell
    :param opcodes_true: list(opcodes) safe
    :param opcodes_false: list(opcodes) safe
    :param br1: list(opcodes) safe
    :param br2: list(opcodes) safe
    :return: list(opcode) safe
    """
    # mem[br1] := mem[cur]; mem[br2] := 0
    # mem[br2] := 1
    # while mem[br1] {
    #   opcodes_true
    #   mem[br1] := 0
    #   mem[br2] := 0
    # }
    # while mem[br2] {
    #   opcodes_false
    #   mem[br2] := 0
    # }
    #
    ops = \
        asm_mov_mul_1(br1, cur, 1, br2) + \
        asm_set_1(br2, 1) + \
        asm_cycle_1(br1,
                    opcodes_true +
                    asm_set_1(br1, 0) +
                    asm_set_1(br2, 0)
                    ) + \
        asm_cycle_1(br2,
                    opcodes_false +
                    asm_set_1(br2, 0))
    return ops

def asm_nop():
    """
    Ничего не делает
    :return: list(opcode) safe
    """
    return low_nop()

