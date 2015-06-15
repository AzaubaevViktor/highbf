__author__ = 'ktulhy'

from compilers.compiler_asmbf.parser.parser import AsmBFParser
from compilers.compiler_asmbf.parser.errors import *
from compilers.compilers_utils.lexer import Lexer

lex = Lexer()
lex.push_source(open("test.bf"), "test.bf")
lex.posix = True

par = AsmBFParser(open("test.bf"))

try:
    par.parse()
except TokenError as e:
    print(e)

par.pretty_print()
