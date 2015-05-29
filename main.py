__author__ = 'ktulhy'

from interpreter.brainfuck import BFInterpreter, ProgramEnd, OpcodeError

inter = BFInterpreter()
inter.load(" ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++"
           ".>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")

print(inter.opcodes._opcodes)

try:
    while 1:
        inter.step()
except ProgramEnd:
    print("\n----------------------\nProgram end")
except OpcodeError:
    print("\n----------------------\nOpcode error")
