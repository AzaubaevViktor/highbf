from unittest import TestCase

__author__ = 'ktulhy'

from compilers.compilers_utils.lexer import Lexer

class TestLexer(TestCase):
    def test(self):
        s = """test 123\t     azaza blahblah
piu piu piu"""

        lex = Lexer(s, " \t\n")
        lex_it = iter(lex)
        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "123"
        assert tok.pos == 6
        assert tok.line == 1
        next(lex_it)
        next(lex_it)
        next(lex_it)
        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "piu"
        assert tok.line == 2
        assert tok.pos == 9

