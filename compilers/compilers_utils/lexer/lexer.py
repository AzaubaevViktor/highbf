__author__ = 'ktulhy'

import shlex


class Token:
    def __init__(self, line=0, text=None, token_type=None):
        self.line = line
        self.text = text
        self.type = token_type

    def typing(self, func):
        if func:
            self.type = func(self)

    def __str__(self):
        return "<`{line}`:\"{text}\"|'{type}'>".format(line=self.line,
                                                       text=self.text,
                                                       type=self.type)

class Lexer(shlex.shlex):
    typing = None
    prev_lineno = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_token(self):
        lineno = self.lineno
        if self.prev_lineno != lineno:
            token = Token(self.prev_lineno, "\n")
            self.prev_lineno = lineno
        else:
            token = Token(lineno, super().get_token())
            print(">>", token)

        token.typing(self.typing)
        return token

    def push_token(self, tok):
        super().push_token(tok.text)
        print("<<", tok)

