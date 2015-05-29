__author__ = 'ktulhy'

class ProgramEnd(Exception):
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
        self.opcodes = [(self.NOP, 0)]
        self.cycles = {}

    def _clean(self, s):
        return [c for c in s if c in "+-><.,[]"]

    def load(self, s):
        self.cycles = {}
        self.opcodes = [(self.NOP, 0)]

        stack = []
        s = self._clean(s)
        pos = 0

        for c in s:
            pos += 1

            if c == "+":
                self._put_opcode((self.ADD, 1))
            elif c == "-":
                self._put_opcode((self.ADD, -1))
            elif c == ">":
                self._put_opcode((self.MOVE, 1))
            elif c == "<":
                self._put_opcode((self.MOVE, -1))
            elif c == ".":
                self._put_opcode((self.WRITE, ))
            elif c == ",":
                self._put_opcode((self.READ, ))
            elif c == "[":
                stack.append(len(self.opcodes))
                self._put_opcode((self.CYCLE_OPEN, -1))
            elif c == "]":
                open_pos = stack.pop()
                opcode = self.opcodes[open_pos]
                self.opcodes[open_pos] = (opcode[0], len(self.opcodes))
                self._put_opcode((self.CYCLE_CLOSE, open_pos))

    def _put_opcode(self, opcode):
        if opcode[0] == self.ADD or opcode[0] == self.MOVE:
            if self.opcodes[-1][0] == opcode[0]:
                last_opcode = self.opcodes[-1]
                self.opcodes[-1] = (last_opcode[0], last_opcode[1] + opcode[1])
            else:
                self.opcodes.append(opcode)
        else:
            self.opcodes.append(opcode)

    def state_clean(self):
        self.MP = 0
        self.PC = 0
        self.mem = [0 for x in range(30000)]

    def step(self):
        if self.PC >= len(self.opcodes):
            raise ProgramEnd
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
            print(chr(self.mem[self.MP]) + str(self.mem[self.MP]), end="")


