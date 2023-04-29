from verse_parser import Parser
from syntaxtree.symboltable import SymbolTable
from syntaxtree.nodes import *
from syntaxtree.parsedNode import ParsedNode
from syntaxtree.sequentor import Sequentor
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

            for i in range(0, len(self.symboltable.symboltable)):
               result =  tree.visit(self.symboltable)
        
        return result