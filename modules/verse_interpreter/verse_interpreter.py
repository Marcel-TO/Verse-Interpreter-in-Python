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
        # --HIER GEÄNDERT damit er er auch beim error ein failnode zurück liefert
        result = None
        if tree != None:
            contexts = Contexts([tree])
            result = contexts.visit(self.symboltable)

            self.symboltable.remove_all_except_self()
            result =  contexts.visit(self.symboltable).visit(self.symboltable)

        return result