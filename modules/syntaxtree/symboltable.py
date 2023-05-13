import string

from structure.tokenTypes import TokenTypes
from structure.logger import Console_Logger

class Symbol:
    def __init__(self, symbol: string, value, symbolType: TokenTypes, insideTable) -> None:
        self.symbol: string = symbol
        self.value = value
        self.symbolType: TokenTypes | None = symbolType
        self.insideTable = insideTable
        self.isUnified = True
    

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

        # Had to set a max iteration count, due to the infinite adding of new symbols during iteration of symbol table while unification especially for the IfNode
        i = 0
        maxIterations = len(self.symboltable)
        while i < maxIterations:
            sym = self.symboltable[i]
            if sym.symbol == symbol and sym.symbolType != None and sym.value == None and value != None and sym.value != sym.symbol:
                occurs = self.U_Occurs(symbol,value)
                if occurs:
                    sym.isUnified = False
                else: sym.value = value
                self.logger.__log__("Added the value: {} to the existing symbol: {} in the symboltable: {}".format(value, sym.symbol, self))
            elif sym.symbol == symbol and sym.symbolType != None and sym.value != None and value != None and sym.value != sym.symbol:
                occurs = self.U_Occurs(symbol,value)
                if occurs:
                    sym.isUnified = False
                else: 
                    isUnified = self.tryUnify(sym.value, value)
                    if isUnified == False:
                        sym.isUnified = isUnified
                    sym.value = value
                
            i += 1  

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
                #if sym.insideTable == symboltable:
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
    
    def checkAllUnificationValid(self):
        for sym in self.symboltable:
            if sym.isUnified == False:
                return False
        return True






    def tryUnify(self, l, r) -> bool:
        try:
            unifiedResult = self.unify(l,r)
            if unifiedResult[0] == False:
                return False
            for u in unifiedResult[1]:
                if u[0].token.type == TokenTypes.IDENTIFIER:
                    if u[1].token.type == TokenTypes.IDENTIFIER and u[0].token.type.value != u[1].token.type.value:
                    
                        nodeR = u[1].visit(self)
                        if nodeR.token.type != TokenTypes.FAIL:
                            self.addValue(u[0].token.value, nodeR)
                    elif u[1].token.type != TokenTypes.IDENTIFIER: self.addValue(u[0].token.value, u[1])
            return True
        except:
            
            lNew = l.visit(self)
            rNew = r.visit(self)
            if lNew.token.type != TokenTypes.FAIL and rNew.token.type != TokenTypes.FAIL:
                unifiedResult = self.unify(lNew,rNew)
                return unifiedResult[0]
            return False
     
    def unify(self,l, r) -> tuple[bool,list]:
      unify_success = (False,"")
      if l.token.type == TokenTypes.INTEGER and r.token.type == TokenTypes.INTEGER:
        unify_success = self.U_LIT(l,r)
      elif (l.token.type == TokenTypes.TUPLE_TYPE and r.token.type == TokenTypes.TUPLE_TYPE) or (l.token.type == TokenTypes.CHOICE and r.token.type == TokenTypes.CHOICE):
        unify_success =  self.U_TUP(l,r)
        
      elif r.token.type == TokenTypes.IDENTIFIER:
        unify_success = self.Hnf_Swap(l,r)
      elif l.token.type == TokenTypes.SCOPE or r.token.type == TokenTypes.SCOPE: 
          if l.token.type == TokenTypes.SCOPE: 
              l = l.nodes[0]
          if r.token.type == TokenTypes.SCOPE: 
              r = r.nodes[0]
          unify_success = self.unify(l,r)  
      else: 
           if l.token.type == TokenTypes.IDENTIFIER and r.token.type == TokenTypes.IDENTIFIER:
                unify_success = self.Var_Swap(l,r)
           else: 
                l = l.visit(self)
                r = r.visit(self)
                if l.token.type != TokenTypes.FAIL and r.token.type != TokenTypes.FAIL:   
                    unify_success = self.unify(l,r)
                else: unify_success = (True, [])
      return unify_success

        


    def U_LIT(self, k1, k2) -> tuple[bool,list]:
      u_str = [k1,k2]
      if k1.token.value != k2.token.value:
        return (False, [])
      return (True, [u_str])

    def U_TUP(self,t1, t2) -> tuple[bool,list]: 
        if len(t1.nodes) != len(t2.nodes):
          return (False, None)

        unified_vals = list(zip(t1.nodes,t2.nodes)) 

        unifiedVals = []
        for uv in unified_vals:
          isUnified = self.unify(uv[0], uv[1])
          if isUnified[0]:
            unifiedVals.extend(isUnified[1])
          else:  return (False, None)
        return (True, unifiedVals)

    def Var_Swap(self,id_l, id_r) -> tuple[bool,list]:
        return (True,[[id_l,id_r],[id_r,id_l]])
      

    def Hnf_Swap(self,l,id_r):
        return (True,[[id_r,l]])
    
    def U_Occurs(self,symbol, val) -> bool:
        for child in val.getChildNodes():
           if child.token.value == symbol:
               return True
        return False
    



    