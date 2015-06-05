__author__ = 'ktulhy'

from compilers.compiler_asmbf.lowlevel_opcode import OpcodeStream

class ProgramEnd(Exception):
    pass

class OpcodeError(Exception):
    pass

class BFInterpreter:
    NOP = 0
    ADD = 1
    MOVE = 2
    CYCLE_OPEN = 3
    CYCLE_CLOSE = 4
    WRITE = 5
    READ = 6
    MP = 0
    PC = 0
    mem = []

    def __init__(self):
        self.state_clean()
        self.opcodes = OpcodeStream()
        self.cycles = {}

    def _clean(self, s):
        return [c for c in s if c in "+-><.,[]"]

    def load(self, s):
        self.cycles = {}
        self.opcodes.clean()

        s = self._clean(s)
        pos = 0

        for c in s:
            pos += 1

            if c == "+":
                self.opcodes.put((self.ADD, 1))
            elif c == "-":
                self.opcodes.put((self.ADD, -1))
            elif c == ">":
                self.opcodes.put((self.MOVE, 1))
            elif c == "<":
                self.opcodes.put((self.MOVE, -1))
            elif c == ".":
                self.opcodes.put((self.WRITE, ))
            elif c == ",":
                self.opcodes.put((self.READ, ))
            elif c == "[":
                self.opcodes.put((self.CYCLE_OPEN, -1))
            elif c == "]":
                self.opcodes.put((self.CYCLE_CLOSE, -1))

    def load_opcodes(self, opcodes):
        self.opcodes = opcodes

    def state_clean(self):
        self.MP = 0
        self.PC = 0
        self.mem = [0 for x in range(30000)]

    def step(self):
        if self.PC >= len(self.opcodes):
            raise ProgramEnd
        if self.PC < 0:
            raise OpcodeError
        opcode = self.opcodes[self.PC]
        self.PC += 1

        if opcode[0] == self.ADD:
            self.mem[self.MP] += opcode[1]
            self.mem[self.MP] %= 256
        elif opcode[0] == self.MOVE:
            self.MP += opcode[1]
        elif opcode[0] == self.CYCLE_OPEN:
            if self.mem[self.MP] == 0:
                self.PC = opcode[1] + 1
        elif opcode[0] == self.CYCLE_CLOSE:
            if self.mem[self.MP] != 0:
                self.PC = opcode[1] + 1
        elif opcode[0] == self.WRITE:
            print(chr(self.mem[self.MP]), end="")


