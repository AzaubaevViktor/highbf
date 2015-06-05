__author__ = 'ktulhy'

class Token:
    def __init__(self, s, line, pos):
        self.s = s.rstrip().lstrip()
        self.line = line
        self.pos = pos

    def __str__(self):
        return "[{}:{}:'{}']".format(self.line, self.pos, self.s)

class Lexer:
    def __init__(self, lines, terminals):
        self.stream = iter("".join(lines))
        self.is_stream_end = False
        self.terminals = terminals
        self._line = 1
        self._pos = 1

    def __next__(self):
        cur_line = self._line
        cur_pos = self._pos
        cur_s = ""

        if self.is_stream_end:
            raise StopIteration

        while 1:
            ch = ""
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
                cur_s += ch

        return Token(cur_s, cur_line, cur_pos)

    def __iter__(self):
        return self
