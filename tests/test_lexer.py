import pytest
from ppc.lexer import Lexer, LexerInput
from ppc.symbol import SymType

import io

class TestLexerInput:
    def test_nextch_simple(self):
        f = io.StringIO("some initial text data")
        l = LexerInput(f)
        assert l.nextch() == 's'
        assert l.current_char == 's'
        assert l.column_position == 1

        assert l.nextch() == 'o'
        assert l.current_char == 'o'
        assert l.column_position == 2

    def test_nextch_end_of_file(self):
        l = LexerInput(io.StringIO("ab"))
        assert l.at_eof == False

        assert l.nextch() == 'a'
        assert l.nextch() == 'b'

        assert l.nextch() == ''
        assert l.current_char == ''
        assert l.column_position == 2
        assert l.at_eof == True
        assert l.at_eol == True

    def test_nextch_end_of_line(self):
        l = LexerInput(io.StringIO("a\nb"))
        assert l.at_eol == False
        assert l.nextch() == 'a'

        l.nextch()  # don't care about returned character
        assert l.at_eol == True

        # next call will clear at_eol and reset the column position
        assert l.nextch() == 'b'
        assert l.column_position == 1
        assert l.at_eol == False

class TestLexer:
    def test_keyword_or_ident(self):
        li = LexerInput(io.StringIO("cat.if ="))
        l = Lexer(li)
        sy = l.insymbol()

        assert(sy.type == SymType.IDENTIFIER)
        assert(sy.str_value == "cat")

        li.nextch()   # kinda lame

        sy = l.keyword_or_ident()
        assert(sy.type == SymType.IFSY)
        assert(sy.str_value == "if")

        # try to trick it
        li = LexerInput(io.StringIO("ify ="))
        l = Lexer(li)
        sy = l.insymbol()
        assert(sy.type == SymType.IDENTIFIER)
        assert(sy.str_value == "ify")

    def test_keyword_or_ident_directly(self):
        # arguably shouldn't test this, but that's how I started
        li = LexerInput(io.StringIO("cat.if ="))
        li.nextch()
        l = Lexer(li)
        sy = l.keyword_or_ident()

        assert(sy.type == SymType.IDENTIFIER)
        assert(sy.str_value == "cat")

        li.nextch() # consume end of word
        sy = l.keyword_or_ident()
        assert(sy.type == SymType.IFSY)
        assert(sy.str_value == "if")

        # try to trick it
        li = LexerInput(io.StringIO("ify ="))
        li.nextch()
        l = Lexer(li)
        sy = l.keyword_or_ident()
        assert(sy.type == SymType.IDENTIFIER)
        assert(sy.str_value == "ify")

    def test_simple_string(self):
        l = Lexer(LexerInput(io.StringIO("'hello'")))
        sy = l.insymbol()
        assert(sy.type == SymType.STRINGCONST)
        assert(sy.str_value == "hello")

