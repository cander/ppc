

class LexerInput:
    def __init__(self, in_file):
        # for the moment, assume these are pulic readable
        self.in_file = in_file
        self.current_char = ' ' # prime the pump with space
        self.line_number = 1
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
    def nextch(self) -> str:
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
    # https://homepages.cwi.nl/~steven/pascal/book/1lexical.html#endofline 
    # We only care about our local state relating to eol
    def process_eol(self):
        self.line_number += 1
        self.column_position = 0
        self.at_eol = False

from ppc.symbol import Symbol, SymType, reserve_to_sym

class Lexer:
    def __init__(self, lexer_input):
        self.lexer_input = lexer_input
        self.errors = []

    # wrappers around FileInput to reduce Demeter violations
    def nextch(self):
        if self.at_eol():
            # maybe we want our own process_eol method?
            self.print_errors()
            self.lexer_input.process_eol()

        return self.lexer_input.nextch()

    def current_char(self):
        return self.lexer_input.current_char

    def at_eol(self) -> bool:
        return self.lexer_input.at_eol

    # https://homepages.cwi.nl/~steven/pascal/book/1lexical.html#insymbol
    def insymbol(self) -> Symbol:
        self.skip_whitespace()
        # check for EOF here?

        # classify
        # see https://homepages.cwi.nl/~steven/pascal/book/9program.html#chartypes
        ch = self.current_char()
        # print(f'insymbol starting at (after skipping whitespace): \'{ch}\'')
        if ch.isalpha():
            sym = self.keyword_or_ident()
            # just return?
            return sym
        elif ch.isdigit():
            print("digit")
            sym = self.number_literal()
            return sym
        # quote
        elif ch == "'":
            return self.string_or_character_literal()
        # colon
        elif ch == ':':
            ch = self.nextch()
            if ch == '=':
                self.nextch() # swallow the '='
                return Symbol(":=", SymType.BECOMES)
            else:
                return Symbol(":", SymType.COLON)
        # less than greater than

    def skip_whitespace(self):
        while self.current_char() in [' ', '\t'] or \
            self.at_eol():
            self.nextch()

    # Record an error based on the error number.  The error numbers are defined in the Pascal standard.
    # Not sure if this needs to be visible outside of th lexer.
    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p338
    def error(self, ferrnr: int):
        # print(f"Error {ferrnr} at line {self.lexer_input.line_number}, column {self.lexer_input.column_position}")
        # currently just use tuple - could be a class
        self.errors.append((ferrnr, self.lexer_input.line_number, self.lexer_input.column_position))

    def error_count(self) -> int:
        # maybe only used for testing
        return len(self.errors)

    def print_errors(self):
        for err in self.errors:
            print(f"Error {err[0]} at line {err[1]}, column {err[2]}")
        self.errors = []

    # get a keyword or identifier after seeing a letter
    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p408
    def keyword_or_ident(self) -> Symbol:
        word = self.current_char()
        # assume identifiers can only be alphanumeric
        while self.nextch().isalnum():
            # allowing identifiers to be unlimited length
            word += self.current_char()

        # look for keywords
        if word in reserve_to_sym:
            return Symbol(word, reserve_to_sym[word])
        else:
            return Symbol(word, SymType.IDENTIFIER)

    # String and character literals are both started with a single quote.
    # A character literal is only one character long.
    # String are longer than one character - no zero-length strings,
    # And, embedded single quotes are represented by two single quotes in a row.
    # Entry condition: current_char is a single quote
    # Exit condition: current_char is past the closing single quote
    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p481
    def string_or_character_literal(self) -> Symbol:
        self.nextch() # skip the opening quote
        literal = ''
        while True:
            ch = self.current_char()
            # watch for EOL
            if self.at_eol():
                # not sure if this is the right way to handle this
                # original code doesn't look like it breaks out code when it sees this
                self.error(202) # string literal not terminated
                return None
            if ch == "'":
                # check for embedded single quote
                if self.nextch() == "'":
                    literal += "'"
                    self.nextch()
                else:
                    break
            else:
                literal += ch
                self.nextch()

        # look for zero-length string
        if literal == '':
            self.error(205) # zero-length string
            return None

        # if the string is one character long, it's a character literal,
        # but it's the same symbol type as a string literal -
        # later code will just check the length. It seems like a
        # character literal ought to be a different symbol type, but
        # whatever.
        return Symbol(literal, SymType.STRINGCONST)

    # https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p426
    def number_literal(self) -> Symbol:
        # integer portion
        num_str = ''
        # worry about maximum length?
        while self.current_char().isdigit():
            num_str += self.current_char()
            self.nextch()
        # look for decimal point and scientific notation
        return Symbol(num_str, SymType.INTCONST, int(num_str))
