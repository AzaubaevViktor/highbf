__author__ = 'ktulhy'

from compilers.compilers_utils.lexer import Lexer
from .bfast import Ast
from .errors import *
from .token_types import *

def typing_token(token):
    s = token.s
    if s == "\n":
        return NEWLINE
    elif s == '':
        return EOF
    elif s == "{":
        return CODEBLOCK_OPEN
    elif s == "}":
        return CODEBLOCK_CLOSE
    elif s == ".":
        return BLOCK
    elif s.find("'") == 0:
        if s.find("'", 1) == len(s) - 1:
            return CHAR
        else:
            raise TokenQuotedError(token)
    elif s.find("\"") == 0:
        if s.find("\"", 1) == len(s) - 1:
            return CHARARR
        else:
            raise TokenQuotedError(token)
    elif s.find("R") == 0 and s[1:].isdigit():
        return REGISTERNAME
    elif s.isdigit():
        return NUMBER

    return STRING

class AsmBFParser:
    def __init__(self, stream):
        self.lexer = Lexer(stream, non_terminals="{}[]")
        self.lexer.typing = typing_token
        self.ast = None

    def parse(self):
        self.ast = Ast(self.lexer)

