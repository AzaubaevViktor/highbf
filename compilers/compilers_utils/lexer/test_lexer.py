from unittest import TestCase

__author__ = 'ktulhy'

from compilers.compilers_utils.lexer import Lexer

class TestLexer(TestCase):
    def test(self):
        s = """


    test 123\t     azaza blahblah


piu piu piu # test azaza

{a } ad{{


"""

        lex = Lexer(s)
        lex.non_terminals = "{}"
        while 1:
            tok = lex.get_token()
            if tok:
                print(tok, end=" ")
            else:
                break

        lex = Lexer(s)
        lex.non_terminals = "{}"

        lex.get_token()
        tok = lex.get_token()
        assert tok.s == "123"
        assert tok.pos == 10
        assert tok.line == 4
        lex.get_token()
        lex.get_token()
        lex.get_token()
        lex.get_token()
        tok = lex.get_token()
        assert tok.s == "piu"
        assert tok.line == 7
        assert tok.pos == 9

        tok = lex.get_token()
        assert tok.s == "{"
        assert tok.pos == 1
        assert tok.line == 9

        lex.get_token()
        tok = lex.get_token()
        assert tok.s == "}"
        assert tok.pos == 4

        lex.get_token()
        tok = lex.get_token()
        assert tok.s == "{"
        assert tok.pos == 8

        tok = lex.get_token()
        assert tok.s == "{"
        assert tok.pos == 9



