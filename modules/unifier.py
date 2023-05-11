from symtable import SymbolTable
from structure.tokenTypes import TokenTypes
from syntaxtree.nodes import *


class Pfushifyer:

  def tryUnify(self, l, r) -> bool: 
      unified = self.unify(l,r)[1]
      for u in unified:
          if u[0].token.type == TokenTypes.IDENTIFIER:
            node:IdentifierNode = u[0]
            SymbolTable.addValue(node.token.value, u[1])
     
  def unify(self,l, r) -> tuple[bool,list[BaseNode]]:
      unify_success = (False,"")
      if l.token.type == TokenTypes.INTEGER and r.token.type == TokenTypes.INTEGER:
        unify_success = self.U_LIT(l,r)
      elif l.token.type == TokenTypes.TUPLE_TYPE and r.token.type == TokenTypes.TUPLE_TYPE:
        unify_success =  self.U_TUP(l,r)
      elif l.token.type == TokenTypes.IDENTIFIER:
        if r.token.type == TokenTypes.IDENTIFIER:
          unify_success = self.Var_Swap(l,r)
        else: 
        # exists = U_Occurs(l,r)
        # if(exists):
        #  return (False,"")
        # else:
            unify_success = self.Assign(l,r)
      elif r.token.type == TokenTypes.IDENTIFIER:
        unify_success = self.Hnf_Swap(l,r)
      return unify_success

        


  def U_LIT(self,k1, k2) -> tuple[bool,list[BaseNode]]:
      u_str = [k1,k2]
      if k1.token.value != k2.token.value:
        return (False, [u_str])
      return (True, [u_str])

  def U_TUP(self,t1, t2) -> tuple[bool,list[BaseNode]]: 
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

  def Var_Swap(self,id_l, id_r) -> tuple[bool,list[BaseNode]]:
    return (True,[[id_l,id_r],[id_r,id_l]])
      

  def Assign(self,id_l, r):
    return (True,[[id_l,r]])

  def Hnf_Swap(self,l,id_r):
    return (True,[[id_r,l]])
  

  


