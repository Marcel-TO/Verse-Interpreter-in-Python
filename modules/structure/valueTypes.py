from enum import Enum
import string

class ValueTypes(Enum):
    # Data
    ANY = "*"
    STRING_TYPE = "string"
    INT_TYPE = "int"
    SEQUENCE_TYPE = "tuple/array"
    FAIL_TYPE = "false?"
    DATA_TYPE = "data"