__author__ = 'ktulhy'

from libs.bf import *

"""Все библиотеки здесь безопасны с точки зрения адресации в памяти.
 Это значит, что они будут правильно работать с mem[0], и после работы MP = 0"""

def asm_set_1(bd, num):
    ops = \
        low_rel_move(0, bd) + \
        low_add(num) + \
        low_rel_move(bd, 0)
    return ops



def asm_mov_1(bd, bn):
    ops = \
        low_rel_move(0, bn) + \
        low_cycle(
            low_block(bn, {
                bn: -1,
                bd: 1
            }, bn)
        ) + \
        low_rel_move(bn, 0)
    return ops

def asm_copy_1(bd, bn, br):
    ops = \
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

