__author__ = 'ktulhy'

from interpreter.brainfuck import BFInterpreter, ProgramEnd

inter = BFInterpreter()
inter.load(" ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++"
           ".>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")

print(inter.opcodes)

try:
    while 1:
        inter.step()
except ProgramEnd:
    print("\n----------------------\nProgram end")
