__author__ = 'ktulhy'

class Token:
    def __init__(self, s, line, pos):
        self.s = s.rstrip().lstrip()
        self.line = line
        self.pos = pos
        self.type = None

    def typing(self, f):
        self.type = f(self)

    def __str__(self):
        return "[{}:{}:'{}']".format(self.line, self.pos, self.s)

class Lexer:
    def __init__(self, lines, terminals=" \n\t", non_terminals=""):
        self.stream = iter("".join(lines))
        self.is_stream_end = False
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.comments = "#"
        self.deferred = None
        self._line = 1
        self._pos = 1
        self.token_queue = []
        self._is_commented = False

    def get_token(self):
        if len(self.token_queue) == 0:
            self._next()

        return self.token_queue.pop()

    def push_token(self, token_str, line=-1, pos=-1):
        self.token_queue.append(Token(token_str, line, pos))

    def _next(self):
        token_line = self._line
        token_pos = self._pos
        token_str = ""

        while 1:
            ch = ""
            if self.deferred:
                token_str = self.deferred
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

            if self._is_commented:
                if self._is_commented != self._line:
                    self._is_commented = False
                else:
                    continue


            if ch in self.terminals:
                if len(token_str) != 0:
                    break
                else:
                    token_pos = self._pos
                    token_line = self._line
            elif ch in self.non_terminals:
                if len(token_str) != 0:
                    self._pos -= 1
                    self.deferred = ch
                    break
                else:
                    token_str = ch
                    break
            elif ch in self.comments:
                self._is_commented = self._line
                continue
            else:
                token_str += ch

        if len(token_str) != 0:
            self.token_queue.append(Token(token_str, token_line, token_pos))
        else:
            self.is_stream_end = True

        if self.is_stream_end:
            self.token_queue.append(None)

    def __iter__(self):
        return self
