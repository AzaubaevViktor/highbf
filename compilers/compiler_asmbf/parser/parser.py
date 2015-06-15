__author__ = 'ktulhy'

from compilers.compilers_utils.lexer import Lexer
from .bfast import Ast
from .errors import *
from .token_types import *

def typing_token(token):
    text = token.text
    if text == "\n":
        return NEWLINE
    elif text == "":
        return EOF
    elif text == "{":
        return CODEBLOCK_OPEN
    elif text == "}":
        return CODEBLOCK_CLOSE
    elif text == ".":
        return BLOCK
    elif text.find("'") == 0:
        if text.find("'", 1) == len(text) - 1:
            return CHAR
        else:
            raise TokenQuotedError(token)
    elif text.find("\"") == 0:
        if text.find("\"", 1) == len(text) - 1:
            return CHARARR
        else:
            raise TokenQuotedError(token)
    elif text.find("R") == 0 and text[1:].isdigit():
        return REGISTERNAME
    elif text.isdigit():
        return NUMBER

    return STRING

class AsmBFParser:
    def __init__(self, stream):
        self.lexer = Lexer()
        self.lexer.instream = stream
        self.lexer.typing = typing_token
        self.ast = None

    def parse(self):
        self.ast = Ast(self.lexer)

    def pretty_print(self):
        self.ast.pretty_print(0)


