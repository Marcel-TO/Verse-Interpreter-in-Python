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


    def interpret(self):
        tree = self.parser.parse()
        result = None
        if tree != None:
            result =  self.visit(tree)

            for i in range(0, len(self.scopetable.scopetable)):
                result =  self.visit(tree)
        
        return result
    

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
        elif isinstance(node, UnaryNode):
                return self.visit_unaryNode(node)
        elif isinstance(node, IdentifierNode):
                return self.visit_identifierNode(node)
        elif isinstance(node, TypeNode):
                return self.visit_typeNode(node)
        elif isinstance(node, SequenceTypeNode):
                return self.visit_typeNodeSequence(node)
        elif isinstance(node, FuncCallNode):
                return self.visit_funcCallNode(node)
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
            return self.visit_choiceSequenceNode(node)
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
        '''
        HIER GEÄNDERT Block Node, darf nur ein Value liefern.
        Bsp. y:= (31|(z:=9; z)); x:=(7|22); (x,y)
        wenn er in diesem Block (z:=9; z) die liste übergibt kommt es später zu einem error.
        Er muss das z zurückgeben, sprich Ein resultat vom Block. 
        '''
        return results[len(results)-1]


    def visit_scopeNode(self, node: ScopeNode):
        for n in node.nodes:
            # remove if Parser is updated!!!!!!
            if type(n) == ParsedNode:
                 self.scopetable.addScope(n.node.token.value, self.visit(node.type))
                 continue
            self.scopetable.addScope(n.token.value, self.visit(node.type))


    def visit_bindingNode(self, node: BindingNode):
        self.scopetable.addBinding(node.leftNode.token.value, node.rightNode, None)
        

    def visit_numberNode(self, node):
        return NumberNode(node.token)
    

    '''
    Operators: +, *, -, /, <, >, <=, >=.

    Fail condition on using following nodes for any 
    of the above listed operations: FaileNode, SequenceNodes (Except choices).

    Operator node, checks its left and right node by visiting it.
    Then in the sequentor it get combination if there is or are many choices
    in the left and right node. Iterates the sequences received by the sequentor and
    return a new node number node or choice node.
    '''
    def visit_operatorNode(self, node):
        fail_conditions = [TokenTypes.FAIL, TokenTypes.TUPLE_TYPE, TokenTypes.ARRAY_TYPE]

        node_left = self.visit(node.leftNode)
        if node_left.token.type in fail_conditions:
                return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))
       
        node_right = self.visit(node.rightNode)
        if node_right.token.type in fail_conditions:
                 return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))

        sequentor = Sequentor([node_left,node_right])
        seqences = sequentor.getSequences()

        # If lenght is one, it can only be two integers.
        if len(seqences) == 1:
            return self.doOperation(seqences[0][0].value,seqences[0][1].value, node.token)
        
        # Else left or/and right node of operation had to be a choice.
        nodes = []
        for s in seqences:
            left_val = s[0]
            right_val = s[1]

            '''
            Checks if left_val or right_val (nodes) are valid for the operation.
            If node save fail node in nodes
            '''
            if (left_val.token.type in fail_conditions) or (right_val.token.type in fail_conditions):
                nodes.append( FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)))
           
            # Else save vale of done operation of left_val and right_val (nodes) into the nodes list.
            else: nodes.append(self.doOperation(left_val.value,right_val.value, node.token))

        # creates the choice
        choice = ChoiceSequenceNode(Token(TokenTypes.CHOICE,TokenTypes.CHOICE.value), nodes)

        '''
        Last visit if choice contains for example (false?|false?).
        in the choice visit method it returns only the values without the false?.
        If there are no valid nodes/values in the choice sequence, it return FailNode.
        ''' 
        return self.visit(choice)


    '''
    Does any of the following operations in the match case
    for two values and returns a new node.
    '''
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
                return SequenceNode(Token(TokenTypes.ARRAY_TYPE, TokenTypes.ARRAY_TYPE), [NumberNode(Token(TokenTypes.INTEGER, i)) for i in range(val1, val2)])   

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

        return  NumberNode(Token(TokenTypes.INTEGER, result))  
    
    '''
    If unary node is called, it calls visitor operator in following way:
    creates multiplication operator node containg -1 and its val it has to multiply.
    '''
    def visit_unaryNode(self, node):

        mul:int = 1
        if node.token.type == TokenTypes.MINUS:
            mul = -1
        return self.visit_operatorNode(OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),
                                                 NumberNode(Token(TokenTypes.INTEGER,mul)),node.node))
            

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


    def visit_funcCallNode(self, node: FuncCallNode):
        pass

    def visit_funcDeclNode(self, node: FuncDeclNode):

        self.scopetable.addBinding(node.identifier.token.value, node.block, node.type)
        pass
    
    
    def visit_forNode(self, node: ForNode):
        if node.condition == None and node.expr == None and node.do == None:
            result = self.visit(node.node)
            if type(result) == ChoiceSequenceNode:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), result.nodes)

            if type(result) == NumberNode:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), [result.token.value])
                
            if result.token.type == TokenTypes.FAIL:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), [])
        
        visited_node = self.visit(node.node)

        if node.condition != None:
            visited_condition = self.visit(node.condition)

        if node.expr != None:
            visited_expr = self.visit(node.expr)
        
        if type(visited_expr) == FailNode:
             return []

        if visited_expr != None:
                return visited_expr
        

    def visit_ifNode(self, node: IfNode):
        result_if = self.visit(node.if_node)
        if result_if != None:
            return self.visit(node.then_node)
        return self.visit(node.else_node)
    

    def visit_rigidEqNode(self, node: RigidEqNode):
        pass


    def visit_flexibleEqNode(self, node: FlexibleEqNode):
        leftResult = self.visit(node.left_node)
        self.scopetable.addValue(leftResult, node.right_node)
             

    def visit_indexingNode(self, node: IndexingNode):
        for scope in self.scopetable.scopetable:
            if node.identifier.token.value == scope.symbol:
                value = self.visit(scope.value)
                if node.index.value >= len(value):
                    print("Exception -> Index out of range")
                    return

                return value[node.index.value]
   

    '''
    Visitor for choice node.
    choices only return nodes/vals which are not false?
    if there is no valid value/node, it returns fail node.
    '''
    def visit_choiceSequenceNode(self,node):
        nodes = []

        # Choice appends all of its sequence, not containing false?
        if node.token.type == TokenTypes.CHOICE:
            for n in node.nodes:
                    current_n = self.visit(n)

                    # Skip fail node
                    if current_n.token.type != TokenTypes.FAIL:
                         nodes.append(current_n)  

            # If choise sequence is empty, return false?
            if(len(nodes) == 0):
                return FailNode(Token(TokenTypes.FAIL,TokenTypes.FAIL.value))
            
            # If choise has atleast one return the node it only contains instead od a choice sequence node.
            if(len(nodes) == 1):
                  # HIER GEÄNDERT  anstatt nodes[0].node nur nodes[0], weil es nur ein node ist und kein visitornode
                 return nodes[0]
            
            # At last, return choice sequence node wit all visited values.

            
            return ChoiceSequenceNode(node.token, nodes)


    '''
    Sequence node, firstly visitis all its nodes and if one node contains false?
    sequence returns fail node, since its invalid.
    If sequence is valid, it gets seqeunces by the sequentor and returns the resulting sequence(ses).
    if sequentor returns many sequences, such as by doing operator node, it means the sequence given to the
    sequentor contained a choice, thus the visitor of sequence node returns a choice sequence node.
    '''
    def visit_sequenceNode(self, node):
        visited_nodes = []
        for n in node.nodes:
            visited_node = self.visit(n)
            if visited_node.token.type == TokenTypes.FAIL:
                return FailNode(TokenTypes.FAIL,TokenTypes.FAIL.value)
            visited_nodes.append(visited_node)
        
        sequentor:Sequentor = Sequentor(visited_nodes)
        sequences = sequentor.getSequences()

        if len(sequences) == 0:
            return FailNode(TokenTypes.FAIL,TokenTypes.FAIL.value)
        
        if len(sequences) == 1:
            return SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),sequences[0])

        seq_nodes = []

        for s in sequences:
            seq_nodes.append(SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),s))

        return ChoiceSequenceNode(Token(TokenTypes.CHOICE,TokenTypes.CHOICE.value),seq_nodes)


    def visit_failNode(self, node: FailNode):
        return FailNode(Token(TokenTypes.FAIL,TokenTypes.FAIL.value))
