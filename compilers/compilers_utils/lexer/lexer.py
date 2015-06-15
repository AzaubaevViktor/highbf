__author__ = 'ktulhy'

class FilePos:
    def __init__(self):
        self._line = 1
        self._pos = 1
        self._prev_pos = 0
        self.backward = 0

    def next(self):
        if self.backward != 0:
            self.backward -= 1
        else:
            self._pos += 1

    def newline(self):
        self._line += 1
        self._prev_pos = self._pos
        self._pos = 0

    def prev(self):
        self.backward += 1

    @property
    def line(self):
        if self.backward == 0:
            return self._line
        else:
            if self._pos - self.backward <= 0:
                return self._line - 1
            else:
                return self._line

    @property
    def pos(self):
        if self.backward == 0:
            return self._pos
        else:
            if self._pos - self.backward <= 0:
                return self._prev_pos - (self._pos - self.backward)
            else:
                return self._pos


class Token:
    def __init__(self, s, line, pos):
        self.s = s.rstrip().lstrip()
        self.line = line
        self.pos = pos
        self.type = None

    def __str__(self):
        return "[{}:{}:'{}']".format(self.line, self.pos, self.s)

def _none_typing(token):
    return None

class Lexer:
    def __init__(self, lines, terminals=" \t", non_terminals="\n"):
        self.stream = iter("".join(lines))
        self.is_stream_end = False
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.comments = "#"
        self.deferred = None
        self._pos = FilePos()
        self.token_queue = []
        self._is_commented = False
        self.typing = _none_typing

    def get_token(self):
        if len(self.token_queue) == 0:
            self._next()

        return self.token_queue.pop()

    def push_token(self, token_str, line=-1, pos=-1):
        self.token_queue.append(Token(token_str, line, pos))

    def _next(self):
        token_line = self._pos.line
        token_pos = self._pos.pos
        token_str = ""

        while 1:
            if self.deferred:
                token_str = self.deferred
                self.deferred = None
                self._pos.next()

            ch = ""

            try:
                ch = next(self.stream)
            except StopIteration:
                self.is_stream_end = True
                break

            if ch == '\n':
                self._pos.newline()

            self._pos.next()

            if self._is_commented:
                if self._is_commented != self._pos.line:
                    self._is_commented = False
                else:
                    continue

            if ch in self.terminals:
                if len(token_str) != 0:
                    break
                else:
                    token_pos = self._pos.pos
                    token_line = self._pos.line
            elif ch in self.non_terminals:
                if len(token_str) != 0:
                    self._pos.prev()
                    self.deferred = ch
                    break
                else:
                    token_str = ch
                    break
            elif ch in self.comments:
                self._is_commented = self._pos.line
                continue
            else:
                token_str += ch

        if len(token_str) != 0:
            tok = Token(token_str, token_line, token_pos)
            tok.type = self.typing(tok)
            self.token_queue.append(tok)
        else:
            self.is_stream_end = True

        if self.is_stream_end:
            self.token_queue.append(None)
