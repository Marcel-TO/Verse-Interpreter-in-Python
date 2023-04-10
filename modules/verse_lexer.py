import string
from structure.token import Token
from structure.tokenTypes import TokenTypes



class lexicon:
    def __init__(self, input: string):
        self.input = input
        self.index = 0
        self.current_char = self.input[self.index]
    
    # moves the pointer a character forward
    def forward(self) -> None:
        self.index += 1

        # checks if index is out of range
        if (self.index >= len(self.input)):
            self.current_char = None
            return
        
        self.current_char = self.input[self.index]
    
    def backward(self) -> None:
        self.index -= 1

        # checks if index is out of range
        if self.index < 0:
            self.current_char = None
            return
        
        self.current_char = self.input[self.index]
    
    def get_int(self) -> int:
        if self.index >= len(self.input):
            return None
        
        result = self.input[self.index]

        # checks if there are multiple digits
        while True:
            self.forward()

            if self.index < len(self.input) and self.input[self.index] != None and self.input[self.index].isnumeric():
                result += self.input[self.index]
            else:
                self.backward()
                break

        return int(result)
    
    def get_var(self) -> string:
        if self.index >= len(self.input):
            return None
        
        result = self.input[self.index]

        # checks if there is a longer variable name
        while True:
            self.forward()

            if self.index < len(self.input) and self.input[self.index] != None and self.input[self.index].isalpha():
                result += self.input[self.index]
            elif self.index < len(self.input) and self.input[self.index] != None and self.input[self.index] == '?':
                result += self.input[self.index]
            else:
                self.backward()
                break
        
        return result
    
    def get_binding(self):
        if self.index >= len(self.input) and self.index + 1 >= len(self.input):
            return None
        
        result = self.input[self.index]
        self.forward()
        
        if self.index < len(self.input) and self.input[self.index] != None:
                result += self.input[self.index]

        match result:
            case TokenTypes.BINDING.value:
                return Token(TokenTypes.BINDING, TokenTypes.BINDING.value)
        
        self.backward()
        return Token(TokenTypes.COLON, TokenTypes.COLON.value)
    
    def get_greater_eq(self):
        if self.index >= len(self.input) and self.index + 1 >= len(self.input):
            return None
        
        result = self.input[self.index]
        self.forward()
        
        if self.index < len(self.input) and self.input[self.index] != None:
                result += self.input[self.index]

        match result:
            case TokenTypes.GREATEREQ.value:
                return Token(TokenTypes.GREATEREQ, TokenTypes.GREATEREQ.value)
        
        self.backward()
        return Token(TokenTypes.GREATER, TokenTypes.GREATER.value)
    
    def get_lower_eq(self):
        if self.index >= len(self.input) and self.index + 1 >= len(self.input):
            return None
        
        result = self.input[self.index]
        self.forward()
        
        if self.index < len(self.input) and self.input[self.index] != None:
                result += self.input[self.index]

        match result:
            case TokenTypes.LOWEREQ.value:
                return Token(TokenTypes.LOWEREQ, TokenTypes.LOWEREQ.value)
        
        self.backward()
        return Token(TokenTypes.LOWER, TokenTypes.LOWER.value)
    
    def get_token(self, char: string) -> Token:
        token = self.check_for_tokentypes(char)

        if token.type != TokenTypes.EOF:
            return token
        
        if char == None:
            return token
            
        # skip spaces.
        if char == ' ':
            self.forward()
            return self.get_token(self.current_char)
        
        if char == TokenTypes.COLON:
            return self.get_next(TokenTypes.BINDING.value)

        # checks if the current character is a number.
        if char.isnumeric():
            result = self.get_int()
            return Token(TokenTypes.INTEGER, result)
        
        if char.isalpha():
            result = self.get_var()
            token = self.check_for_tokentypes(result)
            if(token.type == TokenTypes.EOF):
                token = Token(TokenTypes.IDENTIFIER, result)  
                  
        return token

    def check_for_tokentypes(self, char: string) -> Token:
        # checks if the current character is a supported token type.
        match char:
            case TokenTypes.INTEGER.value:
                return Token(TokenTypes.INTEGER, TokenTypes.INTEGER.value)
            case TokenTypes.IDENTIFIER.value:
                return Token(TokenTypes.IDENTIFIER, TokenTypes.IDENTIFIER.value)
            case TokenTypes.INT_TYPE.value:
                return Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value)
            case TokenTypes.TUPLE_TYPE.value:
                return Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value)
            case TokenTypes.ARRAY_TYPE.value:
                return Token(TokenTypes.ARRAY_TYPE, TokenTypes.ARRAY_TYPE.value)
            case TokenTypes.FAIL.value:
                return Token(TokenTypes.FAIL, TokenTypes.FAIL.value)
            case TokenTypes.PLUS.value:
                return Token(TokenTypes.PLUS, TokenTypes.PLUS.value)
            case TokenTypes.MINUS.value:
                return Token(TokenTypes.MINUS, TokenTypes.MINUS.value)
            case TokenTypes.MULTIPLY.value:
                return Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value)
            case TokenTypes.DIVIDE.value:
                return Token(TokenTypes.DIVIDE, TokenTypes.DIVIDE.value)
            case TokenTypes.GREATER.value:
                return self.get_greater_eq()
            case TokenTypes.GREATEREQ.value:
                return Token(TokenTypes.GREATEREQ, TokenTypes.GREATEREQ.value)
            case TokenTypes.LOWER.value:
                return self.get_lower_eq()
            case TokenTypes.LOWEREQ.value:
                return Token(TokenTypes.LOWEREQ, TokenTypes.LOWEREQ.value)
            case TokenTypes.CHOICE.value:
                return Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value)
            case TokenTypes.FOR.value:
                return Token(TokenTypes.FOR, TokenTypes.FOR.value)
            case TokenTypes.DO.value:
                return Token(TokenTypes.DO, TokenTypes.DO.value)
            case TokenTypes.IF.value:
                return Token(TokenTypes.IF, TokenTypes.IF.value)
            case TokenTypes.THEN.value:
                return Token(TokenTypes.THEN, TokenTypes.THEN.value)
            case TokenTypes.ELSE.value:
                return Token(TokenTypes.ELSE, TokenTypes.ELSE.value)
            case TokenTypes.EOF.value:
                return Token(TokenTypes.EOF, TokenTypes.EOF.value)
            case TokenTypes.COLON.value:
                return self.get_binding()
            case TokenTypes.COMMA.value:
                return Token(TokenTypes.COMMA, TokenTypes.COMMA.value)
            case TokenTypes.SEMICOLON.value:
                return Token(TokenTypes.SEMICOLON, TokenTypes.SEMICOLON.value)
            case TokenTypes.BINDING.value:
                return Token(TokenTypes.BINDING, TokenTypes.BINDING.value)
            case TokenTypes.LBRACKET.value:
                return Token(TokenTypes.LBRACKET, TokenTypes.LBRACKET.value)
            case TokenTypes.RBRACKET.value:
                return Token(TokenTypes.RBRACKET, TokenTypes.RBRACKET.value)
            case TokenTypes.SBL.value:
                return Token(TokenTypes.SBL, TokenTypes.SBL.value)
            case TokenTypes.SBR.value:
                return Token(TokenTypes.SBR, TokenTypes.SBR.value)
            case TokenTypes.CBL.value:
                return Token(TokenTypes.CBL, TokenTypes.CBL.value)
            case TokenTypes.CBR.value:
                return Token(TokenTypes.CBR, TokenTypes.CBR.value)
            case TokenTypes.EQUAL.value:
                return Token(TokenTypes.EQUAL, TokenTypes.EQUAL.value)
            case TokenTypes.SCOPE.value:
                return Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value)
            case TokenTypes.DOT.value:
                return Token(TokenTypes.DOT, TokenTypes.DOT.value)
            case _:
                return Token(TokenTypes.EOF, None)