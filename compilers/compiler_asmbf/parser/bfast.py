from abc import abstractmethod

__author__ = 'ktulhy'

from .token_types import *
from .errors import *

blocks = {}

class AstBlockAbstract:
    lexer = None
    body = None

    def __init__(self, lexer):
        self.lexer = lexer
        self._check()
        self.body = []
        self._parse()

    def _check(self):
        tok = self.lexer.get_token()
        if tok.type != NEWLINE:
            raise NeedNewLine(tok)

    def put_node(self, node):
        self.body.append(node)

    @abstractmethod
    def _parse(self):
        pass


class Ast(AstBlockAbstract):
    def _parse(self):
        while 1:
            tok = self.lexer.get_token()
            if tok.type == BLOCK:
                self.put_node(self.gen_block())
            elif tok.type == EOF:
                return
            else:
                raise TokenOutsideBlock(tok)

    def _check(self):
        pass

    def gen_block(self):
        token = self.lexer.get_token()
        block_name = token.text
        return blocks[block_name](self.lexer)

# Blocks

class AstBlockUsing(AstBlockAbstract):
    def _parse(self):
        pass


class AstBlockData(AstBlockAbstract):
    def _parse(self):
        pass


class AstBlockFn(AstBlockAbstract):
    subblocks = {"code": AstSubBlockCode}

    def _parse(self):
        while 1:
            tok1 = self.lexer.get_token()
            if tok1.type != BLOCK:
                raise NeedBlockOrSubBlock(tok1)

            if tok1.type == EOF:
                self.lexer.push_token(tok1)
                return

            tok2 = self.lexer.get_token()

            if tok2.type == STRING or tok2.type == EOF:
                self.lexer.push_token(tok2)
                self.lexer.push_token(tok1)
                return

            if tok2.type != BLOCK:
                raise NeedBlockOrSubBlock(tok2)

            # tok1 & tok2 is BLOCKs

            key = self.lexer.get_token()

            self.put_node(self.subblocks[key](self.lexer))

# Code Subblocks

class AstSubBlockCode(AstBlockAbstract):
    def _parse(self):
        pass


blocks["using"] = AstBlockUsing
blocks["data"] = AstBlockData
blocks["fn"] = AstBlockFn
