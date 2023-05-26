import string
from structure.token.token import Token
from structure.tokenTypes.tokenTypes import TokenTypes


class lexicon:
    def __init__(self, input: string):
        self.input = input
        self.index = 0
        self.current_char = self.input[self.index]
    
    def reset(self):
        self.index = 0
        self.current_char = self.input[self.index]
    
    # moves the pointer a character forward
    def forward(self) -> None:
        self.index += 1

        # checks if index is out of range
        if self.index >= len(self.input):
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
    
    def get_a_string_from_input(self) -> string:
        result = self.input[self.index]
        self.forward()
        
        if self.index < len(self.input) and self.input[self.index] != None:
                result += self.input[self.index]
        return result
    
    def get_longer_token(self, currentToken: Token) -> Token:
        if self.index + 2 > len(self.input):
            return currentToken
        self.forward()
        nextChar = self.input[self.index]

        newToken = self.get_token(currentToken.value + nextChar)
        if newToken.type != TokenTypes.EOF:
            return newToken
        
        self.backward()
        return currentToken
    
   
    def get_token(self, char: string) -> Token:
        token = self.check_for_tokentypes(char)

        if token.type != TokenTypes.EOF:
            return token
        
        if char == None:
            return token

        # checks if the current character is a number.
        if char.isnumeric():
            result = self.get_int()
            return Token(TokenTypes.INTEGER, result)
        
        if char.isalpha():
            result = self.get_var()
            token = self.check_for_tokentypes(result)
            if(token.type == TokenTypes.DATA):
                return token
            elif(token.type == TokenTypes.EOF):
                token = Token(TokenTypes.IDENTIFIER, result)

        if char == ".":
            self.forward()
            token = self.check_for_tokentypes(char + self.current_char)
        return token

    def check_for_tokentypes(self, char: string) -> Token:
        # checks if the current character is a supported token type.
        if char == TokenTypes.INTEGER.value:
            return Token(TokenTypes.INTEGER, TokenTypes.INTEGER.value)
        elif char == TokenTypes.STRING.value:
            return Token(TokenTypes.STRING, TokenTypes.STRING.value)
        elif char == TokenTypes.IDENTIFIER.value:
            return Token(TokenTypes.IDENTIFIER, TokenTypes.IDENTIFIER.value)
        elif char == TokenTypes.INT_TYPE.value:
            return Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value)
        elif char == TokenTypes.STRING_TYPE.value:
            return Token(TokenTypes.STRING_TYPE, TokenTypes.STRING_TYPE.value)
        elif char == TokenTypes.TUPLE_TYPE.value:
            return Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value)
        elif char == TokenTypes.ARRAY_TYPE.value:
            return Token(TokenTypes.ARRAY_TYPE, TokenTypes.ARRAY_TYPE.value)
        elif char == TokenTypes.FAIL.value:
            return Token(TokenTypes.FAIL, TokenTypes.FAIL.value)
        elif char == TokenTypes.PLUS.value:
            return Token(TokenTypes.PLUS, TokenTypes.PLUS.value)
        elif char == TokenTypes.MINUS.value:
            return Token(TokenTypes.MINUS, TokenTypes.MINUS.value)
        elif char == TokenTypes.MULTIPLY.value:
            return Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value)
        elif char == TokenTypes.DIVIDE.value:
            return Token(TokenTypes.DIVIDE, TokenTypes.DIVIDE.value)
        elif char == TokenTypes.GREATER.value:
            return self.get_longer_token(Token(TokenTypes.GREATER, TokenTypes.GREATER.value))
        elif char == TokenTypes.GREATEREQ.value:
            return Token(TokenTypes.GREATEREQ, TokenTypes.GREATEREQ.value)
        elif char == TokenTypes.LOWER.value:
            return self.get_longer_token(Token(TokenTypes.LOWER, TokenTypes.LOWER.value))
        elif char == TokenTypes.LOWEREQ.value:
            return Token(TokenTypes.LOWEREQ, TokenTypes.LOWEREQ.value)
        elif char == TokenTypes.CHOICE.value:
            return Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value)
        elif char == TokenTypes.FOR.value:
            return Token(TokenTypes.FOR, TokenTypes.FOR.value)
        elif char == TokenTypes.DO.value:
            return Token(TokenTypes.DO, TokenTypes.DO.value)
        elif char == TokenTypes.IF.value:
            return Token(TokenTypes.IF, TokenTypes.IF.value)
        elif char == TokenTypes.THEN.value:
            return Token(TokenTypes.THEN, TokenTypes.THEN.value)
        elif char == TokenTypes.ELSE.value:
            return Token(TokenTypes.ELSE, TokenTypes.ELSE.value)
        elif char == TokenTypes.EOF.value:
            return Token(TokenTypes.EOF, TokenTypes.EOF.value)
        elif char == TokenTypes.COLON.value:
            return self.get_longer_token(Token(TokenTypes.COLON, TokenTypes.COLON.value))
        elif char == TokenTypes.COMMA.value:
            return Token(TokenTypes.COMMA, TokenTypes.COMMA.value)
        elif char == TokenTypes.SEMICOLON.value:
            return Token(TokenTypes.SEMICOLON, TokenTypes.SEMICOLON.value)
        elif char == TokenTypes.BINDING.value:
            return Token(TokenTypes.BINDING, TokenTypes.BINDING.value)
        elif char == TokenTypes.LBRACKET.value:
            return Token(TokenTypes.LBRACKET, TokenTypes.LBRACKET.value)
        elif char == TokenTypes.RBRACKET.value:
            return Token(TokenTypes.RBRACKET, TokenTypes.RBRACKET.value)
        elif char == TokenTypes.SBL.value:
            return Token(TokenTypes.SBL, TokenTypes.SBL.value)
        elif char == TokenTypes.SBR.value:
            return Token(TokenTypes.SBR, TokenTypes.SBR.value)
        elif char == TokenTypes.CBL.value:
            return Token(TokenTypes.CBL, TokenTypes.CBL.value)
        elif char == TokenTypes.CBR.value:
            return Token(TokenTypes.CBR, TokenTypes.CBR.value)
        elif char == TokenTypes.EQUAL.value:
            return self.get_longer_token(Token(TokenTypes.EQUAL, TokenTypes.EQUAL.value))
        elif char == TokenTypes.SCOPE.value:
            return Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value)
        elif char == TokenTypes.DOT.value:
            return self.get_longer_token(Token(TokenTypes.DOT, TokenTypes.DOT.value))
        elif char == TokenTypes.DOTDOT.value:
            return Token(TokenTypes.DOTDOT, TokenTypes.DOTDOT.value)
        elif char == TokenTypes.LAMBDA.value:
            return Token(TokenTypes.LAMBDA, TokenTypes.LAMBDA.value)
        elif char == TokenTypes.SPACE.value:
            return Token(TokenTypes.SPACE, TokenTypes.SPACE.value)
        elif char == TokenTypes.DATA.value:
            return Token(TokenTypes.DATA, TokenTypes.DATA.value)
        return Token(TokenTypes.EOF, TokenTypes.EOF.value)

if __name__ == '__main__':
    lexer = lexicon(". .. data")

    while lexer.current_char is not None:
        token = lexer.get_token(lexer.current_char)
        print(str(token.value) + " is of the tokentype: " + str(token.type))
        lexer.forward()