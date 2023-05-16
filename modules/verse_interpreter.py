from verse_parser import Parser
from syntaxtree.symboltable import SymbolTable
from syntaxtree.nodes import *
from structure.logger import *

class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.symboltable = SymbolTable(None)
    
    def reset(self):
        self.parser.reset()


    def interpret(self):
        tree = self.parser.parse()
        try:
            if tree.hasSyntaxError:
                return
        except:
            result = None
            if tree != None:
                result =  tree.visit(self.symboltable)

            
            
                self.symboltable.remove_all_except_self()
                result =  tree.visit(self.symboltable)
            
        
        return result