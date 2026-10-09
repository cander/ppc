import pytest
from ppc.lexer import LexerInput

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
