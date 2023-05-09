from verse_parser import Parser
from syntaxtree.symboltable import SymbolTable
from syntaxtree.nodes import *
from structure.logger import *

class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.symboltable = SymbolTable()


    def interpret(self):
        tree = self.parser.parse()
        result = None
        if tree != None:
            result =  tree.visit(self.symboltable)

            i = 0
            while i < len(self.symboltable.symboltable):
                self.symboltable.remove_all_except_self()
                result =  tree.visit(self.symboltable)
                i += 1
        
        return result