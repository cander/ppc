import pytest
from ppc.lexer import nextch

def test_A():
    assert nextch() == 'A'
