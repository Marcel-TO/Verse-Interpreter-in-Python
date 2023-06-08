from tokenTypes import TokenTypes

class Token:
    def __init__(self, type: TokenTypes, value) -> None:
        self.type = type
        self.value = value
    
    def __info__(self):
         return "{}: {}".format(self.type, self.value)