from enum import Enum, auto

# https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p80
# "symbol" is an enum that includes all of the reserved words, some of which
# get truncated to fit within the maximum identifier length of 8 characters.
# I'm following that without the truncation
class SymType(Enum):
    # KEYWORD = auto() # keywords aren't a type of symbol
    IDENTIFIER = auto()
    IFSY = auto()
    DOSY = auto()
    OFSY = auto()
    TOSY = auto()
    INSY = auto()
    ORSY = auto()
    ENDSY = auto()
    FORSY = auto()
    VARSY = auto()
    DIVSY = auto()
    MODSY = auto()
    SETSY = auto()
    ANDSY = auto()
    NOTSY = auto()
    THENSY = auto()
    ELSESY = auto()
    WITHSY = auto()
    GOTOSY = auto()
    CASESY = auto()
    TYPESY = auto()
    FILESY = auto()
    BEGINSY = auto()
    UNTILSY = auto()
    WHILESY = auto()
    ARRAYSY = auto()
    CONSTSY = auto()
    LABELSY = auto()
    REPEATSY = auto()
    RECORDSY = auto()
    DOWNTOSY = auto()
    PACKEDSY = auto()
    FORWARDSY = auto()
    PROGRAMSY = auto()
    FUNCTIONSY = auto()
    PROCEDURESY = auto()

# map reserve words to SymTypes
# This is basically handled with a small, fancy data structure at
# https://homepages.cwi.nl/~steven/pascal/book/pcom.html#p3824
# We're just gonna use a simple dictonary
reserve_to_sym = {
    'if'       : SymType.IFSY,
    'do'       : SymType.DOSY,
    'of'       : SymType.OFSY,
    'to'       : SymType.TOSY,
    'in'       : SymType.INSY,
    'or'       : SymType.ORSY,
    'end'      : SymType.ENDSY,
    'for'      : SymType.FORSY,
    'var'      : SymType.VARSY,
    'div'      : SymType.DIVSY,
    'mod'      : SymType.MODSY,
    'set'      : SymType.SETSY,
    'and'      : SymType.ANDSY,
    'not'      : SymType.NOTSY,
    'then'     : SymType.THENSY,
    'else'     : SymType.ELSESY,
    'with'     : SymType.WITHSY,
    'goto'     : SymType.GOTOSY,
    'case'     : SymType.CASESY,
    'type'     : SymType.TYPESY,
    'file'     : SymType.FILESY,
    'begin'    : SymType.BEGINSY,
    'until'    : SymType.UNTILSY,
    'while'    : SymType.WHILESY,
    'array'    : SymType.ARRAYSY,
    'const'    : SymType.CONSTSY,
    'label'    : SymType.LABELSY,
    'repeat'   : SymType.REPEATSY,
    'record'   : SymType.RECORDSY,
    'downto'   : SymType.DOWNTOSY,
    'packed'   : SymType.PACKEDSY,
    'forward'  : SymType.FORWARDSY,
    'program'  : SymType.PROGRAMSY,
    'function' : SymType.FUNCTIONSY,
    'procedure': SymType.PROCEDURESY,
}

class Symbol:
    def __init__(self, str_value: str, type: SymType):
        self.str_value = str_value
        self.type = type
        # maybe track the location where we found this
