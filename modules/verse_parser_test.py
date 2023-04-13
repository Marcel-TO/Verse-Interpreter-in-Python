import string
import unittest
from ddt import ddt, data, file_data, idata, unpack
from structure.token import Token
from structure.tokenTypes import TokenTypes
from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser

@ddt
class ParserTest(unittest.TestCase):
    @data({'input': "7+3", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))},
          {'input': "2*10", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10)))},
          {'input': "90-65", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 90)), NumberNode(Token(TokenTypes.INTEGER, 65)))})
    @unpack
    def test_operator_tree(self, input: string, expected: BaseNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        opNode: OperatorNode = self.parser.parse().node
        self.assertTrue(type(opNode) == type(expected))
        self.assertTrue(opNode.token.value == expected.token.value)
        self.assertTrue(type(opNode.leftNode) == type(expected.leftNode))
        self.assertTrue(opNode.leftNode.value == expected.leftNode.value)
        self.assertTrue(type(opNode.rightNode) == type(expected.rightNode))
        self.assertTrue(opNode.rightNode.value == expected.rightNode.value)
    

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)       