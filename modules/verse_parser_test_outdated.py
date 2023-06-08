import string
import unittest

from ddt import ddt, data, unpack
from parsedNode import ParsedNode
from token import Token
from tokenTypes import TokenTypes
from nodes import *
from verse_lexer import lexicon
from verse_parser import Parser

@ddt
class ParserTest(unittest.TestCase):


    '''
    TEST: OPERATOR NODE
    '''

    @data({'input': "7+3", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))},
          {'input': "2*10", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10)))},
          {'input': "90-65", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 90)), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "2<10", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10)))},
          {'input': "90>65", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 90)), NumberNode(Token(TokenTypes.INTEGER, 65)))})
        
    @unpack
    def test_operator_tree(self, input: string, expected: BaseNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: OperatorNode = self.parser.parse().node

        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.value == expected.token.value) &
                  (type(actual.leftNode) == type(expected.leftNode)) &
                  (actual.leftNode.value == expected.leftNode.value) &
                  (type(actual.rightNode) == type(expected.rightNode)) &
                  (actual.rightNode.value == expected.rightNode.value))

        self.assertTrue(isTrue)

    @data({'input': "(x:=3) + 65", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "- 65 + 90", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "+ 65 + 90", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "(if(1) then 2 else 3) + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2,2) + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2|2) + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(x:=2; 2) + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "x:int + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "false? + 4", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),  NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "- 65 - 90", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "+ 65 - 90", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "(x:=3)-65", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "(if(1) then 2 else 3) - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2,2) - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2|2) - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(x:=2; 2) - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "x:int - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "false? - 4", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),  FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),  NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "- 65 * 90", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "+ 65 * 90", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "(x:=3)*65", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "(if(1) then 2 else 3) * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2,2) * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2|2) * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(x:=2; 2) * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "x:int * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "false? * 4", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),  FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),  NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "- 65 < 90", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "+ 65 < 90", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "(x:=3)<65", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "(if(1) then 2 else 3) < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2,2) < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2|2) < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(x:=2; 2) < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "x:int < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "false? < 4", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),  FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),  NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "- 65 > 90", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "+ 65 > 90", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))), NumberNode(Token(TokenTypes.INTEGER, 90)))},
          {'input': "(x:=3)>65", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 65)))},
          {'input': "(if(1) then 2 else 3) > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2,2) > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(2|2) > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "(x:=2; 2) > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "x:int > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)), NumberNode(Token(TokenTypes.INTEGER, 4)))},
          {'input': "false? > 4", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),  FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),  NumberNode(Token(TokenTypes.INTEGER, 4)))})
    @unpack
    def test_operator_tree_containing_binding_left(self, input: string, expected: OperatorNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: OperatorNode = self.parser.parse().node

        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.type == expected.token.type) &
                  (type(actual.leftNode) == type(expected.leftNode)) &
                  (repr(actual.leftNode) == repr(expected.leftNode)) &
                  (type(actual.rightNode) == type(expected.rightNode)) &
                  (actual.rightNode.value == expected.rightNode.value))

        self.assertTrue(isTrue)


    @data({'input': "65 + x:=3", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 65)),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "90 +- 65", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "90 ++ 65", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "4 + if(1) then 2 else 3", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 + (2,2)", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 + (2|2)", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 + (x:=2; x)", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "4 + x:int", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "4 + false?", 'expected': OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "90 -- 65", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "90 -+ 65", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "65 - x:=3", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 65)),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 - if(1) then 2 else 3", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 - (2,2)", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 - (2|2)", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 - (x:=2; x)", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "4 - x:int", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "4 - false?", 'expected': OperatorNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 4)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "90 * -65", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "90 * +65", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "65 * x:=3", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 65)),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 * if(1) then 2 else 3", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 * (2,2)", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 * (2|2)", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 * (x:=2; x)", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "4 * x:int", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "4 * false?", 'expected': OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 4)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "90 < -65", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "90 < +65", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "65 < x:=3", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 65)),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 < if(1) then 2 else 3", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 < (2,2)", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 < (2|2)", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 < (x:=2; x)", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "4 < x:int", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "4 < false?", 'expected': OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "90 > -65", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "90 > +65", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value),NumberNode(Token(TokenTypes.INTEGER, 90)),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 65))))},
          {'input': "65 > x:=3", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 65)),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 > if(1) then 2 else 3", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "4 > (2,2)", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 > (2|2)", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "4 > (x:=2; x)", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "4 > x:int", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "4 > false?", 'expected': OperatorNode(Token(TokenTypes.GREATER, TokenTypes.GREATER.value), NumberNode(Token(TokenTypes.INTEGER, 4)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))})
    @unpack
    def test_operator_tree_containing_binding_right(self, input: string, expected: OperatorNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: OperatorNode = self.parser.parse().node
        
        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.type == expected.token.type) &
                  (type(actual.rightNode) == type(expected.rightNode)) &
                  (repr(actual.rightNode) == repr(expected.rightNode)) &
                  (type(actual.leftNode) == type(expected.leftNode)) &
                  (actual.leftNode.value == expected.leftNode.value))
  
        self.assertTrue(isTrue)


    @data({'input': "! + 4"},
          {'input': "4 + 2d"},
          {'input': "* + >"},
          {'input': "> 1"},
          {'input': "< 1"})
    @unpack
    def test_operator_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)











    '''
    TEST: BLOCK NODE
    '''

    @data({'input': "(1;2;3)", 'expected': BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_block_tree_multiple_nodes(self, input: string, expected: SequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: SequenceNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (type(actual.nodes[0]) == type(expected.nodes[0])) &
                  (repr(actual.nodes[0]) == repr(expected.nodes[0])) &
                  (type(actual.nodes[1]) == type(expected.nodes[1])) &
                  (repr(actual.nodes[1]) == repr(expected.nodes[1])) &
                  (type(actual.nodes[2]) == type(expected.nodes[2])) &
                  (repr(actual.nodes[2]) == repr(expected.nodes[2]))) 
        
        self.assertTrue(isTrue)

    @data({'input': "(1;false?)", 'expected': BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))])},
          {'input': "(1;7+3)", 'expected': BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))])},
          {'input': "(1;(2,3))", 'expected': BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))])])},
          {'input': "((1|2);3)", 'expected': BlockNode([ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2))]),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "(x:=2;3)", 'expected': BlockNode([BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value),IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "(x:int;3)", 'expected': BlockNode([ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:=1;x);x)", 'expected': BlockNode([BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 1))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]),IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))])},
          {'input': "(1;(if (1) then 2 else 3))", 'expected': BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_block_tree_containing_certain_nodes(self, input: string, expected: SequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: SequenceNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (type(actual.nodes[0]) == type(expected.nodes[0])) &
                  (repr(actual.nodes[0]) == repr(expected.nodes[0])) &
                  (type(actual.nodes[1]) == type(expected.nodes[1])) &
                  (repr(actual.nodes[1]) == repr(expected.nodes[1])))
    
        self.assertTrue(isTrue)
    
   

    @data({'input': "(2,3;2)"},
          {'input': ";"},
          {'input': "1;2;"},
          {'input': ";x:int; x"})
    @unpack
    def test_block_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)














    '''
    TEST: CHOICE NODE
    '''
    @data({'input': "(1|2|3)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_choice_tree_containing_many_choices(self, input: string, expected: ChoiceSequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ScopeNode = self.parser.parse().node

        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.type == expected.token.type) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (actual.nodes[0].value == expected.nodes[0].value) &
                  (actual.nodes[1].value == expected.nodes[1].value) &
                  (actual.nodes[2].value == expected.nodes[2].value))
  
        self.assertTrue(isTrue)

    
    @data({'input': "(1|false?)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))])},
          {'input': "(1|(2,3))", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))])])},
          {'input': "((1|2)|3)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2))]),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:=2)|3)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value),IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:int)|3)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          #{'input': "((x:=1;x)|2)", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 1))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]),NumberNode(Token(TokenTypes.INTEGER, 2))])},
          {'input': "(1|(if (1) then 2 else 3))", 'expected': ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_choice_tree_containing_certain_nodes(self, input: string, expected: ChoiceSequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ChoiceSequenceNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (type(actual.nodes[0]) == type(expected.nodes[0])) &
                  (repr(actual.nodes[0]) == repr(expected.nodes[0])) &
                  (type(actual.nodes[1]) == type(expected.nodes[1])) &
                  (repr(actual.nodes[1]) == repr(expected.nodes[1]))) 
        
        self.assertTrue(isTrue)



    @data({'input': "1|"},
          {'input': "|1"},
          {'input': "|>"},
          {'input': "*|"},
          {'input': "||2|3"})
    @unpack
    def test_choice_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)












    '''
    TEST: FUNC-CALL NODE
    '''

    @data({'input': "f()", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[])})
    @unpack
    def test_func_call_tree_containing_nothing(self, input: string, expected: FuncCallNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncCallNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.args) == len(expected.args)))

        self.assertTrue(isTrue)

    @data({'input': "a(1,2,3)", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"a")),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_func_call_tree_multiple_nodes(self, input: string, expected: FuncCallNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncCallNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.args) == len(expected.args)) &
                  (type(actual.args[0]) == type(expected.args[0])) &
                  (repr(actual.args[0]) == repr(expected.args[0])) &
                  (type(actual.args[1]) == type(expected.args[1])) &
                  (repr(actual.args[1]) == repr(expected.args[1])) &
                  (type(actual.args[2]) == type(expected.args[2])) &
                  (repr(actual.args[2]) == repr(expected.args[2]))) 
        
        self.assertTrue(isTrue)

    @data({'input': "f(false?)", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))])},
          {'input': "f(7+3)", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))])},
          {'input': "f((2,3))", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))])])},
          {'input': "f((1|2))", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2))])])},
          {'input': "f(x:=2)", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value),IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2)))])},
          {'input': "f(x:int)", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))])},
          {'input': "f((x:=1;x))", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 1))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))])])},
          {'input': "f((if (1) then 2 else 3))", 'expected': FuncCallNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_func_call_tree_containing_certain_nodes(self, input: string, expected: FuncCallNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncCallNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.args) == len(expected.args)) &
                  (type(actual.args[0]) == type(expected.args[0])) &
                  (repr(actual.args[0]) == repr(expected.args[0])))

        self.assertTrue(isTrue)
    
   

    @data({'input': "2(1,2)"},
          {'input': "f(1,2"})
    @unpack
    def test_func_call_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)










    '''
    TEST: FUNC-DECL NODE
    '''

    @data({'input': "f():= 2", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,NumberNode(Token(TokenTypes.INTEGER, 2)))},
          {'input': "f():= 7 + 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():= x:=3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():= if(1) then 2 else 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():= (2,2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():= (2|2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():= (x:=2; x)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():= x:int", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "f():= false?", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,None,FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))})
    @unpack
    def test_func_decl_tree_containing_no_params_only_binding(self, input: string, expected: FuncDeclNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncDeclNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.params) == len(expected.params)) &
                  (actual.type == expected.type) &
                  (actual.usesLambda == expected.usesLambda) &
                  (type(actual.block) == type(expected.block)))

        self.assertTrue(isTrue)


    @data({'input': "f(x:int, y:int):= 2", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,NumberNode(Token(TokenTypes.INTEGER, 2)))},
          {'input': "f(x:int, y:int):= 7 + 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):= x:=3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):= if(1) then 2 else 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):= (2,2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):= (2|2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):= (x:=2; x)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):= x:int", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "f(x:int, y:int):= false?", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,None,FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))})
    @unpack
    def test_func_decl_tree_containing_params_only_binding(self, input: string, expected: FuncDeclNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncDeclNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.params) == len(expected.params)) &
                  (type(actual.params[0]) == type(expected.params[0])) &
                  (repr(actual.params[0]) == repr(expected.params[0])) &
                  (type(actual.params[1]) == type(expected.params[1])) &
                  (repr(actual.params[1]) == repr(expected.params[1])) &
                  (type(actual.type) == type(expected.type)) &
                  (actual.usesLambda == expected.usesLambda) &
                  (type(actual.block) == type(expected.block)))

        self.assertTrue(isTrue)




    @data({'input': "f():int := 2", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),NumberNode(Token(TokenTypes.INTEGER, 2)))},
          {'input': "f():int := 7 + 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():int := x:=3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():int := if(1) then 2 else 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f():int := (2,2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():int := (2|2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():int := (x:=2; x)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f():int := x:int", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "f():int := false?", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))})
    @unpack
    def test_func_decl_tree_containing_no_params_but_type_and_binding(self, input: string, expected: FuncDeclNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncDeclNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.params) == len(expected.params)) &
                  (type(actual.type) == type(expected.type)) &
                  (repr(actual.type) == repr(expected.type)) &
                  (actual.usesLambda == expected.usesLambda) &
                  (type(actual.block) == type(expected.block)))
        
        print(actual.identifier.token.value == expected.identifier.token.value)
        print(actual.type == expected.type)
        print(repr(actual.type) == repr(expected.type))
        print(actual.usesLambda == expected.usesLambda)
        print(type(actual.block) == type(expected.block))
        if(isTrue == False):
            print()
        self.assertTrue(isTrue)


    @data({'input': "f(x:int, y:int):int := 2", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),NumberNode(Token(TokenTypes.INTEGER, 2)))},
          {'input': "f(x:int, y:int):int := 7 + 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):int := x:=3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):int := if(1) then 2 else 3", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "f(x:int, y:int):int := (2,2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):int := (2|2)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):int := (x:=2; x)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "f(x:int, y:int):int := x:int", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "f(x:int, y:int):int := false?", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))],False,TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))})
   
    @unpack
    def test_func_decl_tree_containing_params_type_and_binding(self, input: string, expected: FuncDeclNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncDeclNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.params) == len(expected.params)) &
                  (type(actual.params[0]) == type(expected.params[0])) &
                  (repr(actual.params[0]) == repr(expected.params[0])) &
                  (type(actual.params[1]) == type(expected.params[1])) &
                  (repr(actual.params[1]) == repr(expected.params[1])) &
                  (type(actual.type) == type(expected.type)) &
                  (repr(actual.type) == repr(expected.type)) &
                  (actual.usesLambda == expected.usesLambda) &
                  (type(actual.block) == type(expected.block)))

        self.assertTrue(isTrue)



    @data({'input': "f:=(x:int=>x+1)", 'expected': FuncDeclNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"f")),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))], True,None,OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 1))))})
    @unpack
    def test_func_decl_tree_containing_lambda(self, input: string, expected: FuncDeclNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: FuncDeclNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (type(actual.identifier) == type(expected.identifier)) &
                  (actual.identifier.token.value == expected.identifier.token.value) &
                  (len(actual.params) == len(expected.params)) &
                  (type(actual.params[0]) == type(expected.params[0])) &
                  (repr(actual.params[0]) == repr(expected.params[0])) &
                  (type(actual.type) == type(expected.type)) &
                  (actual.usesLambda == expected.usesLambda) &
                  (type(actual.block) == type(expected.block)) &
                  (repr(actual.block) == repr(expected.block)))

        self.assertTrue(isTrue)
   

    @data({'input': "f():="},
          {'input': "2():="},
          {'input': "f():= :int"},
          {'input': "f():int"})
    @unpack
    def test_func_decl_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)














        
    '''
    TEST: IF NODE
    '''
    
    @data({'input': "if (x:int) then y:int else z:int", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "z"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "if (x:int) then { y:int } else { z:int }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "z"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "if (1; 2) then (1; 2) else (1; 2)", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]), BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]))},
          {'input': "if (1; 2) then { 1; 2 } else { 1; 2 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]), BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),BlockNode([NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]))},  
          {'input': "if (3=2) then 1 else 2", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),RigidEqNode(Token(TokenTypes.EQUAL, TokenTypes.EQUAL.value),NumberNode(Token(TokenTypes.INTEGER,3)),NumberNode(Token(TokenTypes.INTEGER,2))),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)))},
          {'input': "if (3=2) then { 1 } else { 2 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),RigidEqNode(Token(TokenTypes.EQUAL, TokenTypes.EQUAL.value),NumberNode(Token(TokenTypes.INTEGER,3)),NumberNode(Token(TokenTypes.INTEGER,2))),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)))},
          {'input': "if (x:=3) then y:=3 else z:=3", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER,3))),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "y")), NumberNode(Token(TokenTypes.INTEGER,3))),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "z")), NumberNode(Token(TokenTypes.INTEGER,3))))},
          {'input': "if (x:=3) then { y:=3 } else { z:=3 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER,3))),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "y")), NumberNode(Token(TokenTypes.INTEGER,3))),BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "z")), NumberNode(Token(TokenTypes.INTEGER,3))))},
          {'input': "if (false?) then false? else false?", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "if (false?) then { false? } else { false? }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))},
          {'input': "if (2<10) then 2*10 else 7+3", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10))),OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10))),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "if (2<10) then { 2*10 } else { 7+3 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),OperatorNode(Token(TokenTypes.LOWER, TokenTypes.LOWER.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10))),OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 10))),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "if (if (1) then 2 else 3) then (if (1) then 2 else 3) else (if (1) then 2 else 3)", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),   IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))))},
          {'input': "if (if (1) then  2 else 3) then { if (1) then 2 else 3 } else { if (1) then 2 else 3 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),   IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),NumberNode(Token(TokenTypes.INTEGER,1)),NumberNode(Token(TokenTypes.INTEGER,2)),NumberNode(Token(TokenTypes.INTEGER,3))))},
          {'input': "if (1|2) then 3|4 else 5|6 ", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 3)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 4)))]),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 5)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 6)))]))},
          {'input': "if (1|2) then { 3|4 } else { 5|6 }", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 3)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 4)))]),ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 5)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 6)))]))},
          {'input': "if ((1,2)) then (3,4) else (5,6) ", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 3)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 4)))]),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 5)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 6)))]))},
          {'input': "if ((1,2)) then { (3,4) } else { (5,6) } ", 'expected': IfNode(Token(TokenTypes.IF, TokenTypes.IF.value),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2)))]),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 3)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 4)))]),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 5)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 6)))]))})
    @unpack
    def test_if_tree(self, input: string, expected: IfNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: IfNode = self.parser.parse().node

        isIfTrue = ((type(actual.if_node) == (type(expected.if_node))) &
                    (repr(actual.if_node) == repr(expected.if_node)))
        
        isThenTrue = ((type(actual.then_node) == (type(expected.then_node))) &
                    (repr(actual.then_node) == (repr(expected.then_node))))
        
        isElseTrue = ((type(actual.else_node) == (type(expected.else_node))) &
                    (repr(actual.else_node) == (repr(expected.else_node))))
        
        isTrue = ((type(actual) == type(expected)) &
                  isIfTrue & isThenTrue & isElseTrue)
    
        self.assertTrue(isTrue)

    
    @data({'input': "if 1 then 2 else 3"},
          {'input': "if then 2 else 3"},
          {'input': "if 1 then else 3"},
          {'input': "if 1 then 2 else "},
          {'input': "if (1} then 2 else 3"},
          {'input': "if {1} then 2 else 3"},
          {'input': "if {1) then 2 else 3"},
          {'input': "if {1 then 2} else 3"},
          {'input': "if {1 then 2 else 3}"},
          {'input': "if (1) then {2) else 3"},
          {'input': "if (1) then (2} else 3"},
          {'input': "if (1) then {2 else 3"},
          {'input': "if (1) then {2 else 3}"},
          {'input': "if (1) then {2} else 3"},
          {'input': "if (1) then {2} else {3"},
          {'input': "if (1) then {2} else {3)"},
          {'input': "if (1) then {2} else (3}"})
    @unpack
    def test_if_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse() 

        self.assertTrue(actual.hasSyntaxError)








    '''
    TEST: SCOPE NODE
    '''

    @data({'input': "x:int", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))},
          {'input': "x:tuple()", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[]))},
          {'input': "x:tuple(int)", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)]))},
          {'input': "x:tuple(int,tuple(int))", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)])]))})
    @unpack
    def test_scope_tree(self, input: string, expected: ScopeNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ScopeNode = self.parser.parse().node
        
        isTrue = ((type(actual) == type(expected)) &
                   (actual.token.type == expected.token.type) &
                   (len(actual.nodes) == len(expected.nodes)) &
                   (type(actual.nodes[0]) == type(expected.nodes[0])) &
                   (actual.nodes[0].token.value == expected.nodes[0].token.value) &
                   (type(actual.type) == type(expected.type)) &
                   (repr(actual.type) == repr(expected.type)))
                   
        
        self.assertTrue(isTrue)

    '''
    TEST: NESTED SCOPE NODE
    '''
    
    @data({'input': "x,y:int", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")),IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE))},
          {'input': "x,y:tuple()", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[]))},
          {'input': "x,y:tuple(int)", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")),IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)]))},
          {'input': "x,y:tuple(int,tuple(int))", 'expected': ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")),IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))], SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE),SequenceTypeNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)])]))})
    @unpack
    def test_nested_scope_tree(self, input: string, expected: BaseNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ScopeNode = self.parser.parse().node
        

        isTrue = ((type(actual) == type(expected)) &
                   (actual.token.type == expected.token.type) &
                   (len(actual.nodes) == len(expected.nodes)) &
                   (type(actual.nodes[0]) == type(expected.nodes[0])) &
                   (actual.nodes[0].token.value == expected.nodes[0].token.value) &
                    (type(actual.nodes[1]) == type(expected.nodes[1])) &
                   (actual.nodes[1].token.value == expected.nodes[1].token.value) &
                   (type(actual.type) == type(expected.type)) &
                   (repr(actual.type) == repr(expected.type)))
                   
        
        self.assertTrue(isTrue)


    @data({'input': "x,y,:int"},
          {'input': "x,y:"},
          {'input': "x:2"},
          {'input': ":"},
          {'input': "x,y:int:tuple(int)"},
          {'input': "y:int:x"},
          {'input': "x:(int)"},
          {'input': "2:int"},
          {'input': "(2,3):int"},
          {'input': "(2;3):int"},
          {'input': "(if(2) then 1 else 2):int"},
          {'input': "(2|3):int"},
          {'input': "(y):int"},
          {'input': "y:false?"})
    @unpack
    def test_scope_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)














    '''
    TEST: SEQUENCE NODE
    '''

    @data({'input': "(1,2,3)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_sequence_tree_containing_certain_nodes(self, input: string, expected: SequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: SequenceNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (type(actual.nodes[0]) == type(expected.nodes[0])) &
                  (repr(actual.nodes[0]) == repr(expected.nodes[0])) &
                  (type(actual.nodes[1]) == type(expected.nodes[1])) &
                  (repr(actual.nodes[1]) == repr(expected.nodes[1])) &
                  (type(actual.nodes[2]) == type(expected.nodes[2])) &
                  (repr(actual.nodes[2]) == repr(expected.nodes[2]))) 
        
        self.assertTrue(isTrue)

    @data({'input': "(1,false?)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))])},
          {'input': "(1,7+3)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 7)), NumberNode(Token(TokenTypes.INTEGER, 3)))])},
          {'input': "(1,(2,3))", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))])])},
          {'input': "((1|2),3)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2))]),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:=2),3)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value),IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:int),3)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)),NumberNode(Token(TokenTypes.INTEGER, 3))])},
          {'input': "((x:=1;x),2)", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 1))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]),NumberNode(Token(TokenTypes.INTEGER, 2))])},
          {'input': "(1,(if (1) then 2 else 3))", 'expected': SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 1)),IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3)))])})
    @unpack
    def test_sequence_tree_containing_certain_nodes(self, input: string, expected: SequenceNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: SequenceNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (len(actual.nodes) == len(expected.nodes)) &
                  (type(actual.nodes[0]) == type(expected.nodes[0])) &
                  (repr(actual.nodes[0]) == repr(expected.nodes[0])) &
                  (type(actual.nodes[1]) == type(expected.nodes[1])) &
                  (repr(actual.nodes[1]) == repr(expected.nodes[1])))
        
        self.assertTrue(isTrue)
    
   

    @data({'input': "(2,3;2)"},
          {'input': "1,2"})
    @unpack
    def test_sequence_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)








    '''
    TEST: UNARY NODE
    '''

    @data({'input': "++3", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "--10", 'expected': UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 10))))},
          {'input': "+-2", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),UnaryNode(Token(TokenTypes.MINUS, TokenTypes.MINUS.value), NumberNode(Token(TokenTypes.INTEGER, 2))))})
    
    @unpack
    def test_unary_tree(self, input: string, expected: UnaryNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: UnaryNode = self.parser.parse().node

        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.value == expected.token.value) &
                  (actual.node.token.value == expected.node.token.value) &
                  (type(actual.node.node) == type(expected.node.node)) & 
                  (repr(actual.node.node) == repr(expected.node.node)))
        
        self.assertTrue(isTrue)

    @data({'input': "+ if(1) then 2 else 3", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "+ x:=3", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),  BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "+ (2,2)", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "+ (2|2)", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "+ (x:=2; x)", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "+ x:int", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))},
          {'input': "+ false?", 'expected': UnaryNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value), FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))}
          )
    @unpack
    def test_unary_tree_containing_other_nodes(self, input: string, expected: UnaryNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: UnaryNode = self.parser.parse().node

        isTrue = ((type(actual) == type(expected)) & 
                  (actual.token.value == expected.token.value) &
                  (type(actual.node) == type(expected.node)) &
                  (repr(actual.node) == repr(expected.node)))
        
        self.assertTrue(isTrue)

    @data({'input': "-"},
          {'input': "+"},
          {'input': "--"},
          {'input': "++"},
          {'input': "-*2"},
          {'input': "+*2"})
    @unpack
    def test_unary_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)
















    '''
    TEST: BINDING NODE
    '''


    @data({'input': "x:= 3", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 3)))},
          {'input': "x:= (2,2)", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "x:= 2|2", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), ChoiceSequenceNode(Token(TokenTypes.CHOICE, TokenTypes.CHOICE.value),[NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))]))},
          {'input': "x:= 2+2", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), OperatorNode(Token(TokenTypes.PLUS, TokenTypes.PLUS.value),NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 2))))},
          {'input': "x:= if(1) then 2 else 3", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), IfNode(Token(TokenTypes.IF, TokenTypes.IF.value), NumberNode(Token(TokenTypes.INTEGER, 1)), NumberNode(Token(TokenTypes.INTEGER, 2)), NumberNode(Token(TokenTypes.INTEGER, 3))))},
          {'input': "z:= (x:=2; x)", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "z")), BlockNode([ BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))]))},
          {'input': "z:= x:=2", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "z")), BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "x")), NumberNode(Token(TokenTypes.INTEGER, 2))))},
          {'input': "z:= x:int", 'expected': BindingNode(Token(TokenTypes.BINDING, TokenTypes.BINDING.value), IdentifierNode(Token(TokenTypes.IDENTIFIER, "z")), ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value), [IdentifierNode(Token(TokenTypes.IDENTIFIER, "x"))], TypeNode(Token(TokenTypes.INT_TYPE, TokenTypes.INT_TYPE.value), ValueTypes.INT_TYPE)))})
    @unpack
    def test_binding_tree_containing_number(self, input: string, expected: BaseNode):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: BindingNode = self.parser.parse().node
        isTrue = ((type(actual) == type(expected)) &
                  (actual.token.type == expected.token.type) &
                  (type(actual.leftNode) == type(expected.leftNode)) &
                  (repr(actual.leftNode) == repr(expected.leftNode)) &
                  (type(actual.rightNode) == type(expected.rightNode)) &
                  (repr(actual.rightNode) == repr(expected.rightNode)))

   

 

    @data({'input': "x,y:=2"},
          {'input': "x:=int"},
          {'input': "1:=2"},
          {'input': ":="},
          {'input': "(2,3):=3"},
          {'input': "(2;2):=3"},
          {'input': "x:int:=3"},
          {'input': "2|3:=3"},
          {'input': "(if (2) then 1 else 2):=3"},
          {'input': "int:=3"})
    @unpack
    def test_binding_tree_wrong_syntax(self, input: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        actual: ParsedNode = self.parser.parse()
        self.assertTrue(actual.hasSyntaxError)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)       