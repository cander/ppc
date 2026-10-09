

class LexerInput:
    def __init__(self, in_file):
        # for the moment, assume these are pulic readable
        self.in_file = in_file
        self.current_char = None
        self.line_number = 0
        self.column_position = 0
        self.at_eof = False

    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p358
    def nextch(self):
        # need eol and eof handling
        self.current_char = self.in_file.read(1)
        self.column_position += 1
        return self.current_char


class Symbol: pass


class Lexer: pass
