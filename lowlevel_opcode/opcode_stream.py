__author__ = 'ktulhy'

from lowlevel_opcode.constants import *

class OpcodeStream:
    _cycle_stack = []
    _opcodes = []

    def __init__(self):
        self.clean()

    def put(self, opcode):
        if opcode[0] == ADD or opcode[0] == MOVE:
            if self._opcodes[-1][0] == opcode[0]:
                last_opcode = self._opcodes[-1]
                self._opcodes[-1] = (last_opcode[0], last_opcode[1] + opcode[1])
                if self._opcodes[-1][1] == 0:
                    del self._opcodes[-1]
            else:
                self._opcodes.append(opcode)
        elif opcode[0] == CYCLE_OPEN:
            self._cycle_stack.append(len(self._opcodes))
            self._opcodes.append(opcode)
        elif opcode[0] == CYCLE_CLOSE:
            open_pos = self._cycle_stack.pop()
            opcode = self._opcodes[open_pos]
            self._opcodes[open_pos] = (opcode[0], len(self._opcodes))
            self._opcodes.append((CYCLE_CLOSE, open_pos))
        else:
            self._opcodes.append(opcode)

    def clean(self):
        self._cycle_stack = []
        self._opcodes = [(NOP, 0)]

    def generate(self):
        pass

    def __getitem__(self, item):
        return self._opcodes[item]

    def __iadd__(self, opcode):
        self.put(opcode)

    def __len__(self):
        return len(self._opcodes)

    def __str__(self):
        return self.generate()