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
            contexts = Contexts([tree])
            result = contexts.visit(self.symboltable)

            self.symboltable.remove_all_except_self()
            result =  contexts.visit(self.symboltable)
            result = result.visit(self.symboltable)

        if(result == None):
            result = FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))

        return result