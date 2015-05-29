from lowlevel_opcode import OpcodeStream

__author__ = 'ktulhy'

from interpreter.brainfuck import BFInterpreter, ProgramEnd, OpcodeError
from libs.native import asm_mov_1, asm_copy_1, asm_set_1

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

print("=================\nMOV:")

inter.state_clean()

opcodes = OpcodeStream()

opcodes += \
    asm_set_1(4, 33) + \
    asm_mov_1(1, 4)

inter.load_opcodes(opcodes)

print(" Opcodes: {}".format(opcodes.get_opcodes()))
print(" Start")
run(inter)
print(" Mem:")
print(" {}".format(inter.mem[0:10]))

print("=================\nCOPY:")

inter.state_clean()

opcodes = OpcodeStream()

opcodes += \
    asm_set_1(4, -1) + \
    asm_copy_1(1, 4, 5)

inter.load_opcodes(opcodes)

print(" Opcodes: {}".format(opcodes.get_opcodes()))
print(" Start")
run(inter)
print(" Mem:")
print(" {}".format(inter.mem[0:10]))

