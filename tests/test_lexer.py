import pytest
from ppc.lexer import LexerInput

import io

def test_nextch():
    f = io.StringIO("some initial text data")
    l = LexerInput(f)
    assert l.nextch() == 's'
    assert l.current_char == 's'

    assert l.nextch() == 'o'
    assert l.current_char == 'o'
