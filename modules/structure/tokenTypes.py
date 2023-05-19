from enum import Enum
import string

class TokenTypes(Enum):
    # Data
    INTEGER = int
    String = "\"" # --HIER GEÄNDERT String Token
    IDENTIFIER = string #Names/Variables
    STRING_TYPE = "string"
    INT_TYPE = "int"
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