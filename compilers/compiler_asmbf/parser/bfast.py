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
        tok = self.get_token()
        if tok.type != NEWLINE:
            raise NeedNewLine(tok)

    def put_node(self, node):
        self.body.append(node)

    def get_token(self):
        return self.lexer.get_token()

    def push_token(self, token):
        self.lexer.push_token(token)

    @abstractmethod
    def _parse(self):
        pass

    def pretty_print(self, level):
        print(" " * level * 2, self.__class__.__name__, sep='')
        for elem in self.body:
            if isinstance(elem, AstBlockAbstract):
                elem.pretty_print(level + 1)
            else:
                print(" " * level * 2, str(elem), sep='')


class Ast(AstBlockAbstract):
    def _parse(self):
        while 1:
            tok = self.get_token()
            if tok.type == BLOCK:
                self.put_node(self.gen_block())
            elif tok.type == EOF:
                return
            else:
                raise TokenOutsideBlock(tok)

    def gen_block(self):
        token = self.get_token()
        block_name = token.text
        return blocks[block_name](self.lexer)


# Blocks

class AstBlockUsing(AstBlockAbstract):
    def _parse(self):
        pass


class AstBlockData(AstBlockAbstract):
    def _parse(self):
        pass

        # Code Subblocks


class AstSubBlockCode(AstBlockAbstract):
    def _parse(self):
        while 1:
            tok = self.get_token()
            if tok.type == CODEBLOCK_OPEN:
                self.put_node(AstSubBlockCode(self.lexer))
            if tok.type == BLOCK or tok.type == CODEBLOCK_CLOSE or tok.type == EOF:
                self.push_token(tok)
                return
            else:
                self.push_token(tok)
                self.put_node(AstSubBlockCodeOperand(self.lexer))


class AstSubBlockCodeOperand(AstBlockAbstract):
    def _parse(self):
        while 1:
            tok = self.get_token()
            if tok.type == EOF or tok.type == BLOCK or tok.type == NEWLINE:
                self.push_token(tok)
                return
            else:
                self.put_node(tok)


class AstBlockFn(AstBlockAbstract):
    subblocks = {"code": AstSubBlockCode}

    def _parse(self):
        while 1:
            tok1 = self.get_token()

            if tok1.type == EOF:
                self.push_token(tok1)
                return

            if tok1.type != BLOCK:
                raise NeedBlockOrSubBlock(tok1)

            tok2 = self.get_token()

            if tok2.type == STRING or tok2.type == EOF:
                self.push_token(tok2)
                self.push_token(tok1)
                return

            if tok2.type != BLOCK:
                raise NeedBlockOrSubBlock(tok2)

            # tok1 & tok2 is BLOCKs

            key = self.get_token()
            if key.text not in self.subblocks:
                raise UnknownBlock(key)

            self.put_node(self.subblocks[key.text](self.lexer))


blocks["using"] = AstBlockUsing
blocks["data"] = AstBlockData
blocks["fn"] = AstBlockFn
