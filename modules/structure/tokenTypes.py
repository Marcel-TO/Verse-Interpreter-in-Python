from enum import Enum
import string

class TokenTypes(Enum):
    # Data
    INTEGER = int
    STRING = "\""
    IDENTIFIER = string #Names/Variables
    INT_TYPE = "int"
    STRING_TYPE = "string"
    TUPLE_TYPE = "tuple"
    ARRAY_TYPE = "array"
    FAIL = "false?"
    # Aritmetics
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    GREATER = ">"
    GREATEREQ = ">="
    LOWER = "<"
    LOWEREQ = "<="
    CHOICE = "|"
    # Mehtods
    FOR = "for"
    DO = "do"
    IF = "if"
    THEN = "then"
    ELSE = "else"
    # Else
    EOF = None
    COLON = ":"
    COMMA=","
    SEMICOLON =";"
    BINDING =":="
    LBRACKET = "("
    RBRACKET = ")"
    SBL = "["
    SBR = "]"
    CBL = "{"
    CBR = "}"
    EQUAL = "="
    SCOPE = ":"
    DOTDOT = ".."
    LAMBDA = "=>"
    SPACE = " "
    DOT = "."
    DATA = "data"