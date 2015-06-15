__author__ = 'ktulhy'

from .token_types import *
from .errors import *

blocks = {}


class Ast:
    def __init__(self, lexer):
        self.lexer = lexer
        self.body = []
        self._parse()

    def _parse(self):
        tok = self.lexer.get_token()
        while 1:
            if tok.type == BLOCK:
                self.put_node(self.gen_block())
            else:
                raise TokenOutsideBlock(tok)

    def put_node(self, node):
        self.body.append(node)


    def gen_block(self):
        token = self.lexer.get_token()
        block_name = token.text
        return blocks[block_name](self.lexer)


class AstBlockUsing:
    def __init__(self, lexer):
        self.lexer = lexer
        self._parse()

    def _parse(self):
        pass


blocks["using"] = AstBlockUsing


class AstBlockData:
    def __init__(self, lexer):
        pass


blocks["data"] = AstBlockData


class AstBlockCode:
    def __init__(self, lexer):
        self.lexer = lexer
        self._parse()

    def _parse(self):
        pass


blocks["code"] = AstBlockCode
