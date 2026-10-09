

class LexerInput:
    def __init__(self):
        # for the moment, assume these are pulic readable
        self.current_char = None
        self.line_number = 0
        self.column_position = 0
        self.at_eof = False

    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p358
    def nextch(self):
        self.current_char = 'A'
        return self.current_char


class Symbol: pass


class Lexer: pass
