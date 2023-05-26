import string
from syntaxtree.nodes.nodes import *
from structure.logger.logger import Console_Logger

class Scope:
    def __init__(self, symbol: string, value: BaseNode, symbolType: TokenTypes, insideTable) -> None:
        self.symbol: string = symbol
        self.value: BaseNode | None = value
        self.symbolType: TokenTypes | None = symbolType
        self.insideTable = insideTable

class ScopeTable:
    def __init__(self) -> None:
        self.scopetable: list[Scope] = []
        self.logger = Console_Logger()
    
    def __info__(self) -> None:
        for scope in self.scopetable:
            self.logger.__log__("Symboltable: Name= {}, Value= {}, type= {} and inside table={}".format(scope.symbol, scope.value, scope.symbolType, scope.insideTable))
    
    def check_if_exists(self, symbol: string, table) -> bool:
        for scope in self.scopetable:
            if scope.symbol == symbol and table == scope.insideTable:
                return True
        return False
    
    def addScope(self, symbol: string, symbolType: TokenTypes) -> None:
        # checks if the name already exists in the current scope. Otherwise add to table.
        if self.check_if_exists(symbol, self) == False:
            self.scopetable.append(Scope(symbol, None, symbolType, self))
            self.logger.__log__("Added the Symbol: {} to the scopetable: {}".format(symbol, self))
    
    def addValue(self, symbol: string, value: BaseNode) -> None:
        # checks if the scope is already defined with type or value.
        for scope in self.scopetable:
            if scope.symbol == symbol and scope.symbolType != None and scope.value == None and value != None:
                scope.value = value
                self.logger.__log__("Added the value: {} to the existing symbol: {} in the scopetable: {}".format(value, scope.symbol, self))
    
    def addBinding(self, symbol: string, value: BaseNode, symbolType: TokenTypes) -> None:
        # checks if the name already exists in the current scope. Otherwise add to table.
        if self.check_if_exists(symbol, self) == False:
            self.scopetable.append(Scope(symbol, value, symbolType, self))
            self.logger.__log__("Added the Symbol: {} to the scopetable: {}".format(symbol, self))
    
    def addScopeTable(self, scopetable) -> None:
            # checks if the name already exists in the current scope. Otherwise add to table.
            for scope in scopetable.scopetable:
                if self.check_if_exists(scope.symbol, scopetable) == False:
                    self.scopetable.append(Scope(scope.symbol, scope.value, scope.symbolType, scopetable))
                    self.logger.__log__("Added the Symbol: {} from the scopetable: {}".format(scope.symbol, scopetable))

    
    def remove(self, symbol:string, value: BaseNode, symbolType: type) -> None:
        # checks if the table is empty.
        if len(self.scopetable) < 1:
            return
        
        # iterates through and removes the corresponding 
        for scope in self.scopetable:
            if scope.symbol == symbol:
                if scope.insideTable == self:
                    self.scopetable.remove(Scope(scope.symbol, scope.value, scope.symbolType, self)) 
                    self.logger.__log__("Removed the Symbol: {} to the scopetable".format(symbol))
    
    def get_value(self, symbol: string, scopetable) -> tuple[bool, BaseNode]:
        for scope in self.scopetable:
            if scope.symbol == symbol:
                if scope.insideTable == scopetable:
                    return True, scope.value
        return False, None