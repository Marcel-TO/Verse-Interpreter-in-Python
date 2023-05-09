import string
from structure.tokenTypes import TokenTypes
from structure.logger import Console_Logger

class Symbol:
    def __init__(self, symbol: string, value, symbolType: TokenTypes, insideTable) -> None:
        self.symbol: string = symbol
        self.value = value
        self.symbolType: TokenTypes | None = symbolType
        self.insideTable = insideTable

class SymbolTable:
    def __init__(self) -> None:
        self.symboltable: list[Symbol] = []
        self.logger = Console_Logger()
    
    def __info__(self) -> None:
        for symbol in self.symboltable:
            self.logger.__log__("Symboltable: Name= {}, Value= {}, type= {} and inside table={}".format(symbol.symbol, symbol.value, symbol.symbolType, symbol.insideTable))
    
    def check_if_exists(self, symbol: string, table) -> bool:
        for sym in self.symboltable:
            if sym.symbol == symbol and table == sym.insideTable:
                return True
        return False
    
    def addScope(self, symbol: string, symbolType: TokenTypes) -> bool:
        # checks if the name already exists in the current symbol. Otherwise add to table.
        if self.check_if_exists(symbol, self) == False:
            self.symboltable.append(Symbol(symbol, None, symbolType, self))
            self.logger.__log__("Added the Symbol: {} to the symboltable: {}".format(symbol, self))
            return True
        return False

    
    def addValue(self, symbol: string, value) -> bool:
        # checks if the symbol is already defined with type or value.
        for sym in self.symboltable:
            if sym.symbol == symbol and sym.symbolType != None and sym.value == None and value != None and sym.value != sym.symbol:
                sym.value = value
                self.logger.__log__("Added the value: {} to the existing symbol: {} in the symboltable: {}".format(value, sym.symbol, self))
                return True
        return False
    
    def addBinding(self, symbol: string, value, symbolType: TokenTypes) -> None:
        # checks if the name already exists in the current symbol. Otherwise add to table.
        if self.check_if_exists(symbol, self) == False:
            self.symboltable.append(Symbol(symbol, value, symbolType, self))
            self.logger.__log__("Added the Symbol: {} to the symboltable: {}".format(symbol, self))
    
    def addSymbolTable(self, symboltable) -> None:
            # checks if the name already exists in the current symbol. Otherwise add to table.
            for sym in symboltable.symboltable:
                if self.check_if_exists(sym.symbol, symboltable) == False:
                    self.symboltable.append(Symbol(sym.symbol, sym.value, sym.symbolType, symboltable))
                    self.logger.__log__("Added the Symbol: {} from the symboltable: {}".format(sym.symbol, symboltable))

    
    def remove(self, symbol:Symbol) -> bool:
        # checks if the table is empty.
        if len(self.symboltable) < 1:
            return False
        
        # iterates through and removes the corresponding 
        for sym in self.symboltable:
            if sym.symbol == symbol.symbol:
                if sym.insideTable == self:
                    self.symboltable.remove(symbol) 
                    self.logger.__log__("Removed the Symbol: {} to the scopetable".format(symbol.symbol))
                    return True
        return False
    

    def remove_all_except_self(self):
        i = 0
        while i < len(self.symboltable):
            if self.symboltable[i].insideTable != self:
                self.logger.__log__("Removed the Symbol: {} from the symboltable".format(self.symboltable[i].symbol))
                self.symboltable.remove(self.symboltable[i])
                i -= 1
            i += 1
    
    def get_value(self, symbol: string, symboltable):
        for sym in self.symboltable:
            if sym.symbol == symbol:
                if sym.insideTable == symboltable:
                    return True, sym.value
        return False, None
    
    def change_value(self, symbol: string, value, symboltable):
        for sym in self.symboltable:
            if sym.symbol == symbol:
                if sym.insideTable == symboltable:
                    sym.value = value
                    return True, sym.value
        return False, None
    

    def clone_table(self):
        newTable = SymbolTable()
        # checks if the name already exists in the current symbol. Otherwise add to table.
        for sym in self.symboltable:
            newTable.symboltable.append(Symbol(sym.symbol, sym.value, sym.symbolType, self))
        return newTable