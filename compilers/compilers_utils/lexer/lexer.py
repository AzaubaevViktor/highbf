__author__ = 'ktulhy'

import shlex


class Token:
    def __init__(self, line=0, text=None, token_type=None):
        self.line = line
        self.text = text
        self.token_type = token_type

    def typing(self, func):
        self.token_type = func(self)

class Lexer(shlex.shlex):
    typing = lambda x: None
    prev_lineno = 0

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)

    def get_token(self):
        lineno = super().lineno
        if self.prev_lineno != lineno:
            return Token(self.prev_lineno, "\n")

        token = Token(super().lineno, super().get_token())
        token.typing(self.typing)
        return token

