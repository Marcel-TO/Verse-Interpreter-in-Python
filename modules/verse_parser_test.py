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
    @data({'input': "7+3", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))})
    @unpack
    def test_syntaxtree(self, input: string, expected: BaseNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        tree = self.parser.parse()
        self.assertTrue(type(tree.node) == type(expected))

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)       