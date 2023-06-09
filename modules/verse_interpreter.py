from verse_parser import Parser
from symboltable import SymbolTable
from nodes import *
from logger import *

class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.symboltable = SymbolTable(None)
    
    def reset_input(self):
        self.parser.reset()
    
    def reset(self):
        self.symboltable = SymbolTable(None)
        self.parser.reset()
       


    def interpret(self):
        tree = self.parser.parse()
        # --HIER GEÄNDERT damit er er auch beim error ein failnode zurück liefert
        result = None
        if tree != None:

            printFunc = PrintDecl(IdentifierNode(Token(TokenTypes.IDENTIFIER,"print")),
                  [ScopeNode(Token(TokenTypes.SCOPE, TokenTypes.SCOPE.value),
                             [IdentifierNode(Token(TokenTypes.IDENTIFIER,"txt"))],
                             TypeNode(Token(TokenTypes.STRING, TokenTypes.STRING.value),ValueTypes.STRING_TYPE))],
                             False,ValueTypes.STRING_TYPE,BlockNode([PrintNode(IdentifierNode(Token(TokenTypes.IDENTIFIER,"txt")))]))
            printFunc.visit(self.symboltable)

            contexts = Contexts([tree])
            result = contexts.visit(self.symboltable)

            self.symboltable.remove_all_except_self()
            result = result.visit(self.symboltable)

        if(result == None or result.token.type == TokenTypes.IDENTIFIER):
            result = FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))

        return result