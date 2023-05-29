from enum import Enum

class ErrorType(Enum):
    SyntaxError = 'Wrong Syntax at'
    SemanticError = 'Wrong Semantics at'
    UnkownError = 'Operation Failure'