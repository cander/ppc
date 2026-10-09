import pytest
from ppc.lexer import LexerInput

def test_nextch():
    l = LexerInput()
    assert l.nextch() == 'A'
    assert l.current_char == 'A'
