from structure.token import Token
from structure.tokenTypes import TokenTypes

class BaseNode:
    def __init__(self, token) -> None:
        self.token = token

class BlockNode(BaseNode):
    def __init__(self, nodes:list[BaseNode]) -> None:
        self.nodes:list[BaseNode] = nodes

class ProgramNode(BaseNode):
    def __init__(self, node:BlockNode) -> None:
        self.node = node

class ScopeNode(BaseNode):
    def __init__(self,token:Token, nodes:list[BaseNode]) -> None:
        super().__init__(token)
        self.nodes = nodes

class BindingNode(BaseNode):
    def __init__(self,token:Token, leftNode:BaseNode, rightNode:BaseNode) -> None:
        super().__init__(token)
        self.leftNode = leftNode
        self.rightNode = rightNode

class NumberNode(BaseNode):
    def __init__(self, token:Token) -> None:
        super().__init__(token)
        self.value = token.value

class OperatorNode(BaseNode):
    def __init__(self, token:Token, leftNode: BaseNode, rightNode: BaseNode) -> None:
        super().__init__(token)
        self.leftNode = leftNode
        self.rightNode = rightNode

class StatementNode(BaseNode):
     def __init__(self, token:Token, leftNode: BaseNode, rightNode: BaseNode) -> None:
        super().__init__(token)
        self.leftNode = leftNode
        self.rightNode = rightNode

class UnaryNode(BaseNode):
     def __init__(self, token:Token, node) -> None:
        super().__init__(token)
        self.node = node

class IdentifierNode(BaseNode):
    def __init__(self, token:Token) -> None: #Change into Variable/IdentifierNode
        super().__init__(token)
        
class ScopeNode(BaseNode):
    def __init__(self, token:Token, nodes:list[BaseNode], type) -> None: #Change into Variable/IdentifierNode
        super().__init__(token)
        self.nodes = nodes
        self.type = type

class TypeNode(BaseNode):
    def __init__(self, token:Token) -> None: 
        super().__init__(token)
        self.type = type

class SequenceTypeNode(TypeNode):
    def __init__(self, token:Token, types:list[TypeNode]) -> None: 
        super().__init__(token)
        self.types = types


class ArgumentsNode: 
    def __init__(self, nodes:list[BaseNode]) -> None: 
        self.nodes = nodes

class FuncCallNode:
    def __init__(self,identifier:IdentifierNode, args:ArgumentsNode) -> None:
        self.identifier = identifier
        self.args = args

class ParamsNode:
    def __init__(self, nodes:list[ScopeNode]) -> None:
        self.nodes = nodes

class FuncDeclNode:
    def __init__(self,identifier:IdentifierNode, nodes:list[ParamsNode],usesLambda:bool, type:TypeNode, block:BlockNode) -> None:
        self.identifier = identifier
        self.nodes = nodes
        self.usesLambda = usesLambda
        self.type = type
        self.block = block

class ForNode(BaseNode):
     def __init__(self, token:Token, node: BaseNode, condition: BaseNode, expr: BaseNode, do: BaseNode) -> None:
        super().__init__(token)
        self.node = node
        self.condition = condition
        self.expr = expr
        self.do = do

class IfNode(BaseNode):
     def __init__(self, token:Token, if_node: BaseNode, then_node: BaseNode, else_node: BaseNode) -> None:
        super().__init__(token)
        self.if_node = if_node
        self.then_node = then_node
        self.else_node = else_node

class RigidEqNode(BaseNode):
     def __init__(self, token:Token, left_node:BaseNode, right_node:BaseNode) -> None:
        super().__init__(token)
        self.left_node = left_node
        self.right_node = right_node

class FlexibleEqNode(BaseNode):
     def __init__(self, token:Token, left_node:BaseNode, right_node:BaseNode) -> None:
        super().__init__(token)
        self.left_node = left_node
        self.right_node = right_node

class SequenceNode(BaseNode):
     def __init__(self, token:Token, nodes:list[BaseNode]) -> None:
        super().__init__(token)
        self.nodes = nodes
        self.seperator = ","
        
     def __repr__(self) -> str:    
        return self.seperator.join([repr(n) for n in self.nodes])

class IndexingNode(BaseNode):
      def __init__(self, token:Token,identifier:IdentifierNode, index:BaseNode) -> None:
        super().__init__(token)
        self.identifier = identifier
        self.index = index

class ChoiceSequenceNode(BaseNode):
    def __init__(self, token:Token, nodes:list[BaseNode]) -> None:
        super().__init__(token)
        self.nodes = nodes
        self.seperator = "|"
        
        self.currentChoice:int = 0 
        self.currentVal:int = - 1 
        self.nodes = nodes
        self.getVals = self.getValsOfChoice()
        
    def __repr__(self) -> str:    
        return self.seperator.join([repr(n) for n in self.nodes])
    
    def getValsOfChoice(self):
        val = []
        current_node = self.nodes[self.currentChoice]
        if self.currentChoice > len(self.nodes) - 1:
            return None
        if current_node.token.type == TokenTypes.CHOICE:
            for v in current_node.yieldVal():
                val.append(v)
            return val
        else: return [current_node]

    def nextChoice(self) -> bool:
        if self.currentChoice + 1 > len(self.nodes) - 1:
            self.setChoiceBack()
            self.setValCountBack()
            return False
        else: 
            self.currentChoice += 1
            self.setValCountBack()
            self.getVals = self.getValsOfChoice()         
            return True     

    def setChoiceBack(self):
        self.currentChoice = 0
        self.setValCountBack()
        self.getVals = self.getValsOfChoice()

    def setValCountBack(self):
        self.currentVal = -1
    
    def getNextVal(self, repeat:bool):
        if self.currentVal + 1 > len(self.getVals) - 1 and repeat: # If first val none, maybe error
            self.setValCountBack()
            self.currentVal += 1
            return self.getVals[self.currentVal]
        elif self.currentVal + 1 > len(self.getVals) - 1: # Need to delete or change this line of code (Not needed)
            return None
        else:
            self.currentVal += 1
            return self.getVals[self.currentVal]
        
    def hasNextVal(self):
        nextValExists = self.currentVal < len(self.getVals) - 1
        return nextValExists

    def yieldVal(self):
        for c in self.nodes:   
            if c.token.type == TokenTypes.CHOICE:
                yield c.yieldVal()
            else: yield c


class FailNode(BaseNode): # Technically not need, since Fail node is 1 to 1 a BaseNode
      def __init__(self, token:Token) -> None:
        super().__init__(token)