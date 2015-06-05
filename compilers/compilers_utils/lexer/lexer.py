__author__ = 'ktulhy'

class Token:
    def __init__(self, s, line, pos):
        self.s = s.rstrip().lstrip()
        self.line = line
        self.pos = pos

    def __str__(self):
        return "[{}:{}:'{}']".format(self.line, self.pos, self.s)

class Lexer:
    def __init__(self, lines, terminals, non_terminals):
        self.lines = "".join(lines)
        self.stream = iter("".join(self.lines))
        self.is_stream_end = False
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.deferred = None
        self._line = 1
        self._pos = 1

    def __next__(self):
        cur_line = self._line
        cur_pos = self._pos
        cur_s = ""

        if self.is_stream_end:
            self.is_stream_end = False
            self.stream = iter(self.lines)
            self._line = 1
            self._pos = 1
            raise StopIteration

        while 1:
            ch = ""
            if self.deferred:
                cur_s = self.deferred
                self.deferred = None
                self._pos += 1
                break

            try:
                ch = next(self.stream)
            except StopIteration:
                self.is_stream_end = True
                break

            if ch == '\n':
                self._line += 1
                self._pos = 0

            self._pos += 1

            if ch in self.terminals:
                if len(cur_s) != 0:
                    break
                else:
                    cur_pos = self._pos
                    cur_line = self._line
            elif ch in self.non_terminals:
                if len(cur_s) != 0:
                    self._pos -= 1
                    self.deferred = ch
                    break
                else:
                    cur_s = ch
                    break
            else:
                cur_s += ch

        if len(cur_s) != 0:
            return Token(cur_s, cur_line, cur_pos)
        else:
            self.is_stream_end = True

    def __iter__(self):
        return self
