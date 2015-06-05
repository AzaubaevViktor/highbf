from unittest import TestCase

__author__ = 'ktulhy'

from compilers.compilers_utils.lexer import Lexer

class TestLexer(TestCase):
    def test(self):
        s = """


    test 123\t     azaza blahblah


piu piu piu

{a } ad{{


"""

        lex = Lexer(s, " \t\n", "[]{}")
        print([str(x) for x in iter(lex)])
        print([str(x) for x in iter(lex)])

        lex_it = iter(lex)
        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "123"
        assert tok.pos == 10
        assert tok.line == 4
        next(lex_it)
        next(lex_it)
        next(lex_it)
        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "piu"
        assert tok.line == 7
        assert tok.pos == 9

        tok = next(lex_it)
        assert tok.s == "{"
        assert tok.pos == 1
        assert tok.line == 9

        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "}"
        assert tok.pos == 4

        next(lex_it)
        tok = next(lex_it)
        assert tok.s == "{"
        assert tok.pos == 8

        tok = next(lex_it)
        assert tok.s == "{"
        assert tok.pos == 9



