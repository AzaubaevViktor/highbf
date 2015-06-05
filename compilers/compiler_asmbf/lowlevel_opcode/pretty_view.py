__author__ = 'ktulhy'

from compilers.compiler_asmbf.lowlevel_opcode.constants import *

def _get_op_str(opcode):
    typ = opcode[0]
    if typ == NOP:
        return "NOP"
    elif typ == ADD:
        return "ADD {}".format(opcode[1])
    elif typ == MOVE:
        return "MOV {}".format(opcode[1])
    elif typ == CYCLE_OPEN:
        return "["
    elif typ == CYCLE_CLOSE:
        return "]"
    elif typ == WRITE:
        return "WRT"
    elif typ == READ:
        return "REA"
    return "UNK"

def get_opcodes_str(opcodes, tab):
    s = ""
    level = 0

    for opcode in opcodes:
        if opcode[0] == CYCLE_CLOSE:
            level -= 1

        s += " " * level * tab + _get_op_str(opcode) + "\n"

        if opcode[0] == CYCLE_OPEN:
            level += 1

    return s