from verse_parser.verse_parser import Parser
from syntaxtree.symboltable.symboltable import SymbolTable
from syntaxtree.nodes.nodes import *
from structure.logger.logger import *

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