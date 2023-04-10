import unittest
from ddt import ddt, data, file_data, idata, unpack

import sys
import os
path = os.path.split(os.path.split(__file__)[0])
newPath = path[0] + '/modules'
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.append(newPath)

from modules.verse_lexer import lexicon

# @ddt
# class LexerTest(unittest.TestCase):
#     # INTEGER = int
#     # IDENTIFIER = string #Names/Variables
       
#     @data({'input': "if", 'expected': Token(TokenTypes.IF,TokenTypes.IF.value)},
#           {'input': ".", 'expected': Token(TokenTypes.DOT,TokenTypes.DOT.value)},
#           {'input': ":", 'expected': Token(TokenTypes.COLON,TokenTypes.COLON.value)},
#           {'input': "=", 'expected': Token(TokenTypes.EQUAL,TokenTypes.EQUAL.value)},
#           {'input': "}", 'expected': Token(TokenTypes.CBR,TokenTypes.CBR.value)},
#           {'input': ":=", 'expected': Token(TokenTypes.BINDING,TokenTypes.BINDING.value)},
#           {'input': "{", 'expected': Token(TokenTypes.CBL,TokenTypes.CBL.value)},
#           {'input': ";", 'expected': Token(TokenTypes.SEMICOLON,TokenTypes.SEMICOLON.value)},
#           {'input': "]", 'expected': Token(TokenTypes.SBR,TokenTypes.SBR.value)},
#           {'input': ",", 'expected': Token(TokenTypes.COMMA,TokenTypes.COMMA.value)},
#           {'input': "[", 'expected': Token(TokenTypes.SBL,TokenTypes.SBL.value)},
#           {'input': ")", 'expected': Token(TokenTypes.RBRACKET,TokenTypes.RBRACKET.value)},
#           {'input': "else", 'expected': Token(TokenTypes.ELSE,TokenTypes.ELSE.value)},
#           {'input': "(", 'expected': Token(TokenTypes.LBRACKET,TokenTypes.LBRACKET.value)},
#           {'input': "then", 'expected': Token(TokenTypes.THEN,TokenTypes.THEN.value)},
#           {'input': "do", 'expected': Token(TokenTypes.DO,TokenTypes.DO.value)},
#           {'input': "for", 'expected': Token(TokenTypes.FOR,TokenTypes.FOR.value)},
#           {'input': "=>", 'expected': Token(TokenTypes.LAMBDA,TokenTypes.LAMBDA.value)},
#           {'input': "|", 'expected': Token(TokenTypes.CHOICE,TokenTypes.CHOICE.value)},
#           {'input': ">", 'expected': Token(TokenTypes.GREATER,TokenTypes.GREATER.value)},
#           {'input': "<", 'expected': Token(TokenTypes.LOWER,TokenTypes.LOWER.value)},
#           {'input': "/", 'expected': Token(TokenTypes.DIVIDE,TokenTypes.DIVIDE.value)},
#           {'input': "*", 'expected': Token(TokenTypes.MULTIPLY,TokenTypes.MULTIPLY.value)},
#           {'input': "-", 'expected': Token(TokenTypes.MINUS,TokenTypes.MINUS.value)},
#           {'input': "+", 'expected': Token(TokenTypes.PLUS,TokenTypes.PLUS.value)},
#           {'input': "false?", 'expected': Token(TokenTypes.FAIL,TokenTypes.FAIL.value)},
#           {'input': "array", 'expected': Token(TokenTypes.ARRAY_TYPE,TokenTypes.ARRAY_TYPE.value)},
#           {'input': "tuple", 'expected': Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value)},
#           {'input': "int", 'expected': Token(TokenTypes.INT_TYPE,TokenTypes.INT_TYPE.value)},
#           {'input': "123", 'expected': Token(TokenTypes.INTEGER,123)},
#           {'input': "arrays", 'expected': Token(TokenTypes.IDENTIFIER,"arrays")},
#           {'input': "tuplde2", 'expected': Token(TokenTypes.IDENTIFIER,"tuplde")},
#           {'input': "", 'expected': Token(TokenTypes.EOF,"")},
#           {'input': None, 'expected': Token(TokenTypes.EOF,"")},
#        )

#     @unpack
#     def test_received_tokens(self, input, expected:Token):
#         self.lexer = lexicon(input)
#         token = self.lexer.get_token(self.lexer.current_char)
#         self.assertTrue(expected.type == token.type and expected.value == token.value)
    

# if __name__ == '__main__':
#     unittest.main(argv=['first-arg-is-ignored'], exit=False)       
