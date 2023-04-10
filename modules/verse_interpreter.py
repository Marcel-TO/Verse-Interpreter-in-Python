from verse_parser import Parser
from syntaxtree.scopetable import ScopeTable
from syntaxtree.nodes import *
from syntaxtree.parsedNode import ParsedNode
from syntaxtree.sequentor import Sequentor
from structure.logger import *

class Interpreter:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.scopetable = ScopeTable()
        self.logger: Logger = Console_Logger()

    def interpret(self):
        tree = self.parser.parse()
        if tree != None:
            return self.visit(tree)
    
    def visit(self, node):
        if isinstance(node, ProgramNode):
                return self.visit_programNode(node)
        elif isinstance(node, BlockNode):
                return self.visit_blockNode(node)
        elif isinstance(node, ScopeNode):
                return self.visit_scopeNode(node)
        elif isinstance(node, BindingNode):
                return self.visit_bindingNode(node)
        elif isinstance(node, OperatorNode):
                return self.visit_operatorNode(node)
        elif isinstance(node, NumberNode):
                return self.visit_numberNode(node)
        elif isinstance(node, StatementNode):
                return self.visit_statementNode(node)
        elif isinstance(node, UnaryNode):
                return self.visit_unaryNode(node)
        elif isinstance(node, IdentifierNode):
                return self.visit_identifierNode(node)
        elif isinstance(node, TypeNode):
                return self.visit_typeNode(node)
        elif isinstance(node, SequenceTypeNode):
                return self.visit_typeNodeSequence(node)
        elif isinstance(node, ArgumentsNode):
                return self.visit_argumentsNode(node)
        elif isinstance(node, FuncCallNode):
                return self.visit_funcCallNode(node)
        elif isinstance(node, ParamsNode):
                return self.visit_paramsNode(node)
        elif isinstance(node, FuncDeclNode):
                return self.visit_funcDeclNode(node)
        elif isinstance(node, ForNode):
            return self.visit_forNode(node)
        elif isinstance(node, IfNode):
            return self.visit_ifNode(node)
        elif isinstance(node, RigidEqNode):
                return self.visit_rigidEqNode(node)
        elif isinstance(node, FlexibleEqNode):
                return self.visit_flexibleEqNode(node)
        elif isinstance(node, SequenceNode):
                return self.visit_sequenceNode(node)
        elif isinstance(node, ChoiceSequenceNode):
            return self.visit_choideSequenceNode(node)
        elif isinstance(node, IndexingNode):
                return self.visit_indexingNode(node)
        elif isinstance(node, ParsedNode):
                return self.visit(node.node)
        elif isinstance(node, FailNode):
                return self.visit_failNode(node)
    
    def visit_programNode(self, node: ProgramNode):
        return self.visit(node.node)

    def visit_blockNode(self, node: BlockNode):
        results = []
        for n in node.nodes:
            result = self.visit(n)
            if result != None:
                 results.append(result)
        
        return results

    def visit_scopeNode(self, node: ScopeNode):
        for n in node.nodes:
            self.scopetable.addScope(n.token.value, None, self.visit(node.type))

    def visit_bindingNode(self, node: BindingNode):
        self.scopetable.addScope(node.leftNode.token.value, node.rightNode, None)
        
    def visit_operatorNode(self, node: OperatorNode):
        val_left = self.visit(node.leftNode)
        val_right = self.visit(node.rightNode)

        # checks if it is a simple math operation.
        if type(val_left) == int and type(val_right) == int:
            return self.doOperation(val_left, val_right, node.token)

        if type(val_left) == BaseNode:
            if val_left.node.token.type == TokenTypes.FAIL:
                return val_left
        else:
             val_left = NumberNode(Token(TokenTypes.INTEGER, val_left))
        if type(val_right) == BaseNode:
            if val_right.node.token.type == TokenTypes.FAIL:
                    return val_right
        else:
             val_right = NumberNode(Token(TokenTypes.INTEGER, val_right))

        return self.GetNodeForOperation(val_left, val_right, node.token)

                
    def GetNodeForOperation(self,val_left,val_right, opToken:Token):
        nodes = []
        token = None

        if val_left.node.token.type == TokenTypes.CHOICE:
            token = val_left.node.token
            for n in val_left.node.nodes:
                if val_right.node.token.type == TokenTypes.CHOICE:
                    for n2 in val_right.node.nodes:
                       node = self.doOperation(n.value,n2.value,opToken)
                       nodes.append(node)
                else:nodes.append(self.doOperation(n.value,val_right.node.token.value,opToken)) 

        elif val_right.node.token.type == TokenTypes.CHOICE:
            token = val_right.node.token
            for n in val_right.node.nodes:
               nodes.append(self.doOperation(n.value,val_left.node.token.value,opToken)) 
               
        elif val_left.node.token.type == TokenTypes.INTEGER and val_right.node.token.type == TokenTypes.INTEGER:
             return self.doOperation(val_left.node.token.value,val_right.node.token.value,opToken)
        return SequenceNode(token, nodes)
                             
    def doOperation(self,val1:int,val2:int, token:Token):
        result = 0
        match token.type:
            case TokenTypes.DIVIDE:
                result = val1 // val2
            case TokenTypes.MULTIPLY:
                result = val1 * val2
            case TokenTypes.PLUS:              
                result = val1 + val2
            case TokenTypes.MINUS:
                result = val1 - val2
            case TokenTypes.DOT:
                return [i for i in range(val1, val2)]   

        if token.type == TokenTypes.EQUAL:
            if type(val1) == type(val2):
                if val1 == val2:
                    result = val1
        
        if token.type == TokenTypes.GREATER:
            if type(val1) == type(val2):
                if val1 > val2:
                    result = val1
        
        if token.type == TokenTypes.LOWER:
            if type(val1) == type(val2):
                if val1 < val2:
                    result = val1
            
        return  result 

    def visit_numberNode(self, node: NumberNode):
        return node.value
    
    def visit_statementNode(self, node: StatementNode):
        pass

    def visit_unaryNode(self, node: UnaryNode):
        pass

    def visit_identifierNode(self, node: IdentifierNode):
        # checks if the identifier already exists in the scopetable.
        for scope in self.scopetable.scopetable:
             if scope.symbol == node.token.value and scope.value != None:
                  return self.visit(scope.value)
        return node.token.value

    def visit_typeNode(self, node: TypeNode):
        return node.token.type

    def visit_typeNodeSequence(self, node: SequenceTypeNode):
        result = []
        for n in node.types:
            result.append(self.visit(n))
        return result

    def visit_argumentsNode(self, node: ArgumentsNode):
        pass

    def visit_funcCallNode(self, node: FuncCallNode):
        pass

    def visit_paramsNode(self, node: ParamsNode):
        pass

    def visit_funcDeclNode(self, node: FuncDeclNode):
        pass
    
    def visit_forNode(self, node: ForNode):
        if node.condition == None and node.expr == None and node.do == None:
            return self.visit(node.node)
        visitted_node = self.visit(node.node)
        
        if node.condition != None:
            visitted_condition = self.visit(node.condition)

        if node.expr != None:
            visitted_expr = self.visit(node.expr)
        
        if visitted_expr != None:
                return visitted_expr

    def visit_ifNode(self, node: IfNode):
        result_if = self.visit(node.if_node)
        if result_if != None:
            return self.visit(node.then_node)
        return self.visit(node.else_node)

    def visit_rigidEqNode(self, node: RigidEqNode):
        pass

    def visit_flexibleEqNode(self, node: FlexibleEqNode):
        leftResult = self.visit(node.left_node)
        self.scopetable.addScope(leftResult, node.right_node, None)
             

    def visit_sequenceNode(self, node: SequenceNode):
        # nodeStatus:NodeStatus = NodeStatus.VALUE_RECEIVABLE
        sequentor:Sequentor = Sequentor(node.nodes) 
        sequences = sequentor.getSequences()
        if len(sequences) == 0:
            return sequences[0]
        return ChoiceSequenceNode(Token(TokenTypes.CHOICE,sequences))

    def visit_indexingNode(self, node: IndexingNode):
        for scope in self.scopetable.scopetable:
            if node.identifier.token.value == scope.symbol:
                value = self.visit(scope.value)
                if node.index.value >= len(value):
                    self.logger.__log__("Exception -> Index out of range")
                    return

                return value[node.index.value]
    
    def visit_choideSequenceNode(self,node):
        # nodes = []

        # # Choice appends all of its sequence, not containing false?
        # if node.token.type == TokenTypes.CHOICE:
        #     for n in node.nodes:
        #             current_n = self.visit(n)

        #             # Do on not assigned value
        #             if current_n.type == NodeStatus.NOT_ASSIGNED_YET:
        #                  nodeStatus = NodeStatus.NOT_ASSIGNED_YET

        #             # Do on error
        #             elif current_n.type == NodeStatus.ERROR:
        #                  nodeStatus = NodeStatus.ERROR
        #                  self.logger.__log__("Error in sequence visitor for CHOICE")
        #                  break 
                    
        #             # Skip fail node
        #             if current_n.node.token.type != TokenTypes.FAIL:
        #                  nodes.append(current_n.node)  

        #     # If choise sequence is empty, return false?
        #     if(len(nodes) == 0):
        #         return VisitorNode(nodeStatus,FailNode(Token(TokenTypes.FAIL,TokenTypes.FAIL.value)))
            
        #     # If choise has atleast one return the node it only contains instead od a choice sequence node.
        #     if(len(nodes) == 1):
        #          return VisitorNode(nodeStatus,nodes[0].node) 
            
        #     # At last, return choice sequence node wit all visited values.
        #     return VisitorNode(nodeStatus,ChoiceSequenceNode(node.token, nodes))
        pass

    def visit_failNode(self, node: FailNode):
        self.logger.__log_error__("Fail", ErrorType.SemanticError)
