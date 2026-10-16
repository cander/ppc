

class LexerInput:
    def __init__(self, in_file):
        # for the moment, assume these are pulic readable
        self.in_file = in_file
        self.current_char = None
        self.line_number = 0
        self.column_position = 0
        self.at_eol = False
        self.at_eof = False

    # https://homepages.cwi.nl/~steven/pascal/book/1lexical.html#nextch
    # Returns the next character in the input stream.
    # Keeps track the current line number and column position
    # At end of line:
    #     at_eol is True, the returned character is undefined,
    #     the line number is incremented, and the column position is reset
    # At end of file, at_eof is True, return ''
    def nextch(self):
        if self.at_eol:
            self.process_eol()
        
        # if we cared about performance, maybe we'd read a line at a time
        self.current_char = self.in_file.read(1)
        if self.current_char == '':
            self.at_eof = True
            self.at_eol = True # EOF is EOL, too
        else:
            self.column_position += 1
            if self.current_char == '\n':
                self.at_eol = True

        return self.current_char

    # This is not the same as - 
    #    ttps://homepages.cwi.nl/~steven/pascal/book/1lexical.html#endofline 
    # We only care about our local state relating to eol
    def process_eol(self):
        self.line_number += 1
        self.column_position = 0
        self.at_eol = False


class Symbol: pass


class Lexer:
    def __init__(self, lexer_input):
        self.lexer_input = lexer_input

    # https://homepages.cwi.nl/~steven/pascal/book/1lexical.html#insymbol
    def insymbol(self):
        self.skip_whitespace()
        # check for EOF?

        # classify
        # see https://homepages.cwi.nl/~steven/pascal/book/9program.html#chartypes
        ch = self.lexer_input.current_char
        if ch.isalpha():
            print("letter")
            sym = self.keyword_or_ident()
            # just return?
        elif ch.isdigit():
            print("digit")
        # quote
        # colon
        # less than greater than


    def skip_whitespace(self):
        while self.lexer_input.current_char in [' ', '\t'] or self.lexer.at_eol:
            self.lexer_input.nextch()

    # get a keyword or identifier after seeing a letter
    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p408
    def keyword_or_ident(self):
        word = self.lexer_input.current_char
        # assume identifiers can only be alphanumeric
        while self.lexer_input.nextch().isalnum():
            # allowing identifiers to be unlimited length
            word += self.lexer_input.current_char

        # look for keywords
        return word # will return a symbol

