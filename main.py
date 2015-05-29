from lowlevel_opcode import OpcodeStream

__author__ = 'ktulhy'

from interpreter.brainfuck import BFInterpreter, ProgramEnd, OpcodeError
from libs.native import *
from libs.math import *
from lowlevel_opcode.pretty_view import get_opcodes_str


def run(interpreter):
    try:
        while 1:
            interpreter.step()
    except ProgramEnd:
        print("\nProgram end")
    except OpcodeError:
        print("\nOpcode error")


inter = BFInterpreter()
inter.load(" ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++"
           ".>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")

print(inter.opcodes.get_opcodes())

run(inter)

print("=================\nIFELSE:")

inter.state_clean()

opcodes = OpcodeStream()

opcodes += \
    asm_set_1(5, 0) + \
    asm_ifelse_1(5,
                 asm_set_1(6, 5),
                 asm_set_1(6, 10),
                 0, 1)

inter.load_opcodes(opcodes)

print(" Opcodes: {}".format(opcodes.get_opcodes()))
print(" Start")
run(inter)
print(" Mem:")
print(" {}".format(inter.mem[0:10]))

print("=================\nREPEAT:")

inter.state_clean()

opcodes = OpcodeStream()

opcodes += \
    asm_set_1(5, 10) + \
    asm_repeat_1(5,
                 asm_add_num_1(6, 10))

inter.load_opcodes(opcodes)

print(" Opcodes: {}".format(opcodes.get_opcodes()))
print(" Start")
run(inter)
print(" Mem:")
print(" {}".format(inter.mem[0:10]))

print("=================\nMATH:")

inter.state_clean()

opcodes = OpcodeStream()

# 4 += 5, overflow in 6
opcodes += \
    asm_set_1(4, -10) + \
    asm_set_1(5, 15) + \
    math_add_1(4, 5, 6, 0, 1)

inter.load_opcodes(opcodes)

print(" Opcodes len={}: {}".format(len(opcodes), get_opcodes_str(opcodes.get_opcodes(), 4)))
print(" Start")
run(inter)
print(" Mem:")
print(" {}".format(inter.mem[0:10]))
