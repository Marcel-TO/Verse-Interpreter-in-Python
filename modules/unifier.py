from unification import unify

from structure.token import Token
from structure.tokenTypes import TokenTypes
from syntaxtree.nodes import *


n1 = NumberNode(Token(TokenTypes.INTEGER, 1))
n2 = NumberNode(Token(TokenTypes.INTEGER, 2))
n3 = NumberNode(Token(TokenTypes.INTEGER, 3))
id1 = IdentifierNode(Token(TokenTypes.IDENTIFIER, "y"))
id2 = IdentifierNode(Token(TokenTypes.IDENTIFIER, "z"))
id3 = IdentifierNode(Token(TokenTypes.IDENTIFIER, "w"))


s0 = SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),[n1,n2])

simple_Table = []
s1 = SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),[id1,n1,n3,s0])
s2 = SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),[n2,id2,n3,s0])


xs = [s1,s2]
simple_Table.append(xs)
symbolTable = SymbolTable()
# ∃x y z. x = ⟨y, 3⟩; x = ⟨2, z⟩; x = (2,3); y
# x = (1,x); x=(1,(2,x))

print(unify(s1,s2))
print(1)

def unify(l, r) -> tuple[bool,str]:
  unify_success = (False,"")
  if l.token.type == TokenTypes.INTEGER and r.token.type == TokenTypes.INTEGER:
   unify_success = U_LIT(l,r)
  elif l.token.type == TokenTypes.TUPLE_TYPE and r.token.type == TokenTypes.TUPLE_TYPE:
   unify_success =  U_TUP(l,r)
  elif l.token.type == TokenTypes.IDENTIFIER:
    if r.token.type == TokenTypes.IDENTIFIER:
      unify_success = Var_Swap(l,r)
    else: unify_success = Assign(l,r)
  elif r.token.type == TokenTypes.IDENTIFIER:
    unify_success = Hnf_Swap(l,r)
  return unify_success

    


def U_LIT(k1, k2) -> tuple[bool,str]:
  u_str = "{}={}".format(k1.token.value,k2.token.value)
  if k1.token.value != k2.token.value:
    return (False, [u_str])
  return (True, [u_str])

def U_TUP(t1, t2) -> tuple[bool,str]:
    
    if len(t1.nodes) != len(t2.nodes):
      return (False, "")

    unified_vals = list(zip(t1.nodes,t2.nodes)) 

    unifiedVals = []
    for uv in unified_vals:
       isUnified = unify(uv[0], uv[1])
       if isUnified[0]:
         unifiedVals.extend(isUnified[1])
       else:  return (False, "")
    return (True, unifiedVals)

def Var_Swap(id_l, id_r) -> tuple[bool,str]:
  return (True,["{}={}".format(repr(id_l),repr(id_r)),
          "{}={}".format(repr(id_r),repr(id_l))])
  

def Assign(id_l, r):
  return (True,["{}={}".format(repr(id_l),repr(r))])

def Hnf_Swap(l,id_r):
  return (True,["{}={}".format(repr(id_r),repr(l))])

print(unify(s1,s2)[1])      

