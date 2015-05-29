__author__ = 'ktulhy'

from libs.bf import *


def asm_mov_1(bd, bn):
    ops = low_rel_move(0, bn) + \
          low_cycle(
              low_dec() +
              low_rel_move(bn, bd) +
              low_inc() +
              low_rel_move(bd, bn)
          ) + \
          low_rel_move(bn, 0)
