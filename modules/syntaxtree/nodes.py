from structure.token import Token
from structure.tokenTypes import TokenTypes
from syntaxtree.symboltable import SymbolTable
from syntaxtree.sequentor import Sequentor


'''
Top class of all nodes.
'''
class BaseNode:
    def __init__(self, token) -> None:
        self.token = token 

    def visit(self, symboltable: SymbolTable):
        pass 

#Class that takes a parsed node, containes information if node could have been parsed
class ParsedNode:
    def __init__(self, node: BaseNode, hasSyntaxError:bool ):
        self.node = node
        self.hasSyntaxError = hasSyntaxError

     
'''
Node for block statements.
'''  
class BlockNode(BaseNode):
    def __init__(self, nodes:list[BaseNode]) -> None:
        self.nodes:list[BaseNode] = nodes
        self.seperator = ";"

    def __repr__(self) -> str:    
        return self.seperator.join([repr(n) for n in self.nodes])
    
    def visit(self, symboltable: SymbolTable):
        results = []
        for n in self.nodes:
            result = n.visit(symboltable)
            if result != None:
                 results.append(result)
        '''
        HIER GEÄNDERT Block Node, darf nur ein Value liefern.
        Bsp. y:= (31|(z:=9; z)); x:=(7|22); (x,y)
        wenn er in diesem Block (z:=9; z) die liste übergibt kommt es später zu einem error.
        Er muss das z zurückgeben, sprich Ein resultat vom Block. 
        '''
        return results[len(results)-1] 


'''
Top Node in tree.
''' 
class ProgramNode(BaseNode):
    def __init__(self, node:BlockNode) -> None:
        self.node = node
    
    def visit(self, symboltable: SymbolTable):
        return self.node.visit(symboltable) 


'''
Node for binded identifiers.
''' 
class BindingNode(BaseNode):
    def __init__(self,token:Token, leftNode:BaseNode, rightNode:BaseNode) -> None:
        super().__init__(token)
        self.leftNode = leftNode
        self.rightNode = rightNode

    def __repr__(self) -> str:    
        return "{}:={}".format(repr(self.leftNode),repr(self.rightNode))  
    
    def visit(self, symboltable: SymbolTable):
        symboltable.addBinding(self.leftNode.token.value, self.rightNode, None)
        return self.rightNode


'''
Node representing a number.
''' 
class NumberNode(BaseNode):
    def __init__(self, token:Token) -> None:
        super().__init__(token)
        self.value = token.value

    def __repr__(self) -> str:
        return str(self.value)
    
    def visit(self, symboltable: SymbolTable):
        return NumberNode(self.token) 


'''
Operators: +, *, -, /, <, >, <=, >=.
Fail condition on using following nodes for any 
of the above listed operations: FaileNode, SequenceNodes (Except choices).
Operator node, checks its left and right node by visiting it.
Then in the sequentor it get combination if there is or are many choices
in the left and right node. Iterates the sequences received by the sequentor and
return a new node number node or choice node.
'''
class OperatorNode(BaseNode):
    def __init__(self, token:Token, leftNode: BaseNode, rightNode: BaseNode) -> None:
        super().__init__(token)
        self.leftNode = leftNode
        self.rightNode = rightNode

    def __repr__(self) -> str:    
        return "({}) {} ({})".format(repr(self.leftNode),self.token.value,repr(self.rightNode))  

    def visit(self, symboltable: SymbolTable):
        fail_conditions = [TokenTypes.FAIL, TokenTypes.TUPLE_TYPE, TokenTypes.ARRAY_TYPE]

        node_left = self.leftNode.visit(symboltable)
        if node_left.token.type in fail_conditions:
                return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))
       
        node_right = self.rightNode.visit(symboltable)
        if node_right.token.type in fail_conditions:
                 return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))

        sequentor = Sequentor([node_left,node_right])
        seqences = sequentor.getSequences()

        # If lenght is one, it can only be two integers.
        if len(seqences) == 1:
            return self.doOperation(seqences[0][0].value,seqences[0][1].value, self.token)
        
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
            else: nodes.append(self.doOperation(left_val.value,right_val.value, self.token))

        # creates the choice
        choice = ChoiceSequenceNode(Token(TokenTypes.CHOICE,TokenTypes.CHOICE.value), nodes)

        '''
        Last visit if choice contains for example (false?|false?).
        in the choice visit method it returns only the values without the false?.
        If there are no valid nodes/values in the choice sequence, it return FailNode.
        ''' 
        return choice.visit(symboltable) 
    
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
            case TokenTypes.GREATER:
                if val1 > val2:
                    result = val1
                else: return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)) 
            case TokenTypes.GREATEREQ:
                if val1 >= val2:
                    result = val1
                else: return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)) 
            case TokenTypes.LOWEREQ:
                if val1 <= val2:
                    result = val1
                else: return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)) 
            case TokenTypes.LOWER:
                if val1 < val2:
                    result = val1
                else: return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value)) 
        return  NumberNode(Token(TokenTypes.INTEGER, result))  

'''
If unary node is called, it calls visitor operator in following way:
creates multiplication operator node containg -1 and its val it has to multiply.
'''
class UnaryNode(BaseNode):
    def __init__(self, token:Token, node) -> None:
        super().__init__(token)
        self.node = node

    def __repr__(self) -> str:    
        return "{}{}".format(self.token.value,repr(self.node)) 

    def visit(self, symboltable: SymbolTable):
        mul:int = 1
        if self.token.type == TokenTypes.MINUS:
            mul = -1
        res = OperatorNode(Token(TokenTypes.MULTIPLY, TokenTypes.MULTIPLY.value),
                                                 NumberNode(Token(TokenTypes.INTEGER,mul)),self.node)
        return res.visit(symboltable)
             

'''
Node for identifiers.
''' 
class IdentifierNode(BaseNode):
    def __init__(self, token:Token) -> None: #Change into Variable/IdentifierNode
        super().__init__(token)

    def __repr__(self) -> str:
        return str(self.token.value)

    def visit(self, symboltable: SymbolTable):
        # checks if the identifier already exists in the scopetable.
        for symbol in symboltable.symboltable:
             if symbol.symbol == self.token.value and symbol.value != None:
                  return symbol.value.visit(symboltable)
        return self 

'''
Node for scoped identifiers.
''' 
class ScopeNode(BaseNode):
    def __init__(self, token:Token, nodes:list[BaseNode], type) -> None: #Change into Variable/IdentifierNode
        super().__init__(token)
        self.nodes = nodes
        self.type = type
        self.seperator = ","

    def __repr__(self) -> str:    
        return "{}{}{}".format(self.seperator.join([repr(n) for n in self.nodes]),self.token.value, repr(self.type)) 

    def visit(self, symboltable: SymbolTable):
        for n in self.nodes:
            # remove if Parser is updated!!!!!!
            if type(n) == ParsedNode:
                 symboltable.addScope(n.node.token.value, self.type.visit(symboltable))
                 continue
            symboltable.addScope(n.token.value, self.type.visit(symboltable)) 

'''
Top class node for types (int, tuple, etc.).
''' 
class TypeNode(BaseNode):
    def __init__(self, token:Token) -> None: 
        super().__init__(token)
        self.type = type

    def __repr__(self) -> str:
        return str(self.token.value)

    def visit(self, symboltable: SymbolTable):
        return self.token.type 

'''
Node for sequence types (tuple).
''' 
class SequenceTypeNode(TypeNode):
    def __init__(self, token:Token, types:list[TypeNode]) -> None: 
        super().__init__(token)
        self.types = types
        self.seperator = ","

    def __repr__(self) -> str:
        if(self.token.type == TokenTypes.TUPLE_TYPE):
            return "tuple({})".format(self.seperator.join([repr(t) for t in self.types]))
        return "array{{}}".format(self.seperator.join([repr(t) for t in self.types]))

    def visit(self, symboltable: SymbolTable):
        result = []
        for n in self.types:
            result.append(n.visit(symboltable))
        return result 

'''
Node for scoped func calls.
''' 
class FuncCallNode:
    def __init__(self,identifier:IdentifierNode, args:list) -> None:
        self.identifier = identifier
        self.args = args

    def visit(self, symboltable: SymbolTable):
        table = SymbolTable()
        scope = symboltable.get_value(self.identifier.token.value, symboltable)
        if scope[0]:
            func_dec:FuncDeclNode = scope[1]
            index = 0
            params = func_dec.params
            for param in params:
                id = param.nodes[0].token.value

                arg = self.args[index].visit(symboltable)
                if(arg.token.type == TokenTypes.IDENTIFIER):
                     arg = None

                table.addBinding(id, arg ,param.type)
                index += 1
            val = func_dec.block.visit(table)

            # Check if a variable is given to argument that has not been set (Logic)
            index = 0
            for arg in self.args:
                 if arg.token.type == TokenTypes.IDENTIFIER:  
                    arg = arg.token.value            
                    id = params[index].nodes[0].token.value
                    param_val_at_arg_pos = table.get_value(id, table)
                    if param_val_at_arg_pos[0]:
                        symboltable.addValue(arg, param_val_at_arg_pos[1])
                 index += 1
            return val

'''
Node for func declarations.
''' 
class FuncDeclNode:
    def __init__(self,identifier:IdentifierNode, params:list[ScopeNode],usesLambda:bool, type:TypeNode, block:BlockNode) -> None:
        self.identifier = identifier
        self.params = params
        self.usesLambda = usesLambda
        self.type = type
        self.block = block

    def visit(self, symboltable: SymbolTable):
        symbol = self.identifier.token.value
        symboltable.addBinding(symbol, self, self.type)


'''
Node for loops.
''' 
class ForNode(BaseNode):
    def __init__(self, token:Token, node: BaseNode, condition: BaseNode, expr: BaseNode, do: BaseNode) -> None:
        super().__init__(token)
        self.node = node
        self.condition = condition
        self.expr = expr
        self.do = do

    def visit(self, symboltable: SymbolTable):
        if self.condition == None and self.expr == None and self.do == None:
            result = self.node.visit(symboltable)
            if type(result) == SequenceNode or type(result) == ChoiceSequenceNode:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), result.nodes)

            if type(result) == NumberNode:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), [result.token.value])
                
            if result.token.type == TokenTypes.FAIL:
                return SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), [])
        
        visited_node = self.node.visit(symboltable)

        if self.condition != None:
            visited_condition = self.condition.visit(symboltable)

        if self.expr != None:
            visited_expr = self.expr.visit(symboltable)
        
        if type(visited_expr) == FailNode:
             return []

        if visited_expr != None:
                return visited_expr 


'''
Node for if statements.
''' 
class IfNode(BaseNode):
    def __init__(self, token:Token, if_node: BaseNode, then_node: BaseNode, else_node: BaseNode) -> None:
        super().__init__(token)
        self.if_node = if_node
        self.then_node = then_node
        self.else_node = else_node

    def __repr__(self) -> str:    
        return "{}({}) then {} else {}".format(self.token.value, repr(self.if_node), repr(self.then_node),  repr(self.else_node))

    def visit(self, symboltable: SymbolTable):
        result_if = self.if_node.visit(symboltable)
        if result_if != None:
            return self.then_node.visit(symboltable)
        return self.else_node.visit(symboltable) 

'''
Node for rigid equals.
''' 
class RigidEqNode(BaseNode):
    def __init__(self, token:Token, left_node:BaseNode, right_node:BaseNode) -> None:
        super().__init__(token)
        self.left_node = left_node
        self.right_node = right_node

    def __repr__(self) -> str:
        return "{}{}{}".format(repr(self.left_node),self.token.value, repr(self.right_node)) 

    def visit(self, symboltable: SymbolTable):
        pass 

'''
Node for flexible equals.
''' 
class FlexibleEqNode(BaseNode):
    def __init__(self, token:Token, left_node:BaseNode, right_node:BaseNode) -> None:
        super().__init__(token)
        self.left_node = left_node
        self.right_node = right_node

    def visit(self, symboltable: SymbolTable):
        leftResult = self.left_node.visit(symboltable)
        symboltable.addValue(leftResult.token.value, self.right_node) 


'''
Node for sequences (tuple, array).
''' 
class SequenceNode(BaseNode):
    def __init__(self, token:Token, nodes:list[BaseNode]) -> None:
        super().__init__(token)
        self.nodes = nodes
        self.seperator = ","
        
    def __repr__(self) -> str:    
        return "(" + self.seperator.join([repr(n) for n in self.nodes]) + ")"

    def visit(self, symboltable: SymbolTable):
        visited_nodes = []
        for n in self.nodes:
            visited_node = n.visit(symboltable)
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


'''
Node for indexing.
''' 
class IndexingNode(BaseNode):
    def __init__(self, token:Token,identifier:IdentifierNode, index:BaseNode) -> None:
        super().__init__(token)
        self.identifier = identifier
        self.index = index

    def visit(self, symboltable: SymbolTable):
        for symbol in symboltable.symboltable:
            if self.identifier.token.value == symbol.symbol:
                value = symbol.value.visit(symboltable)
                if self.index.value >= len(value):
                    print("Exception -> Index out of range")
                    return

                return value[self.index.value] 


'''
Node for choices sequences(branches of a listing of choices).
''' 
class ChoiceSequenceNode(BaseNode):
    def __init__(self, token:Token, nodes:list[BaseNode]) -> None:
        super().__init__(token)
        self.nodes = nodes
        self.seperator = "|"
        
        # Current choice branch/nodes index.
        self.currentChoice:int = 0 

        # Current val index for current choice branch/nodes.
        self.currentVal:int = - 1 

        # Gets the vals of current choice branch.
        self.getVals = self.getValsOfChoice() #--> Need to do something different
        
    def __repr__(self) -> str:    
        return "(" + self.seperator.join([repr(n) for n in self.nodes]) + ")"

    def visit(self, symboltable: SymbolTable):
        nodes = []

        # Choice appends all of its sequence, not containing false?
        if self.token.type == TokenTypes.CHOICE:
            for n in self.nodes:
                    current_n = n.visit(symboltable)

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
            return ChoiceSequenceNode(self.token, nodes) 
    

    '''
    Gets the vals of the current choice branch.
    ''' 
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

    '''
    Steps to the next choice if possible.
    
    If:
    no choice branches available (Index of choice is at the last choice branch),
    set choice branch index back to the beginning choice branch, choice branch at index 0
    and set back the index counter for the values of the choice branch at current index.
    Return False indicating, no choice branches left.
    Else:
    
    Step to the next choice branch.
    Set counter back, so it can start at the beginning of the current choice branch, as
    soon get next val method is called.
    Return True indicating next choice branch has been selected.
    ''' 
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


    '''
    Set back the current choice branch index to 0 and its value index also to its starting integer value.
    '''
    def setChoiceBack(self):
        self.currentChoice = 0
        self.setValCountBack()
        self.getVals = self.getValsOfChoice()


    '''
    Sets the val to -1, so when get next val is called, its steps forward to index 0. 
    '''
    def setValCountBack(self):
        self.currentVal = -1
    

    '''
    Gets the next val of current choice branch. Repeats the selection of a choice branch, if requested.
    Needs to repeat the values for a choice branch, except for the last choices node during operation.
    '''
    def getNextVal(self, repeat:bool):
        if self.currentVal + 1 > len(self.getVals) - 1 and repeat: # If first val none, maybe error
            self.setValCountBack()
            self.currentVal += 1
            return self.getVals[self.currentVal]
        else:
            self.currentVal += 1
            return self.getVals[self.currentVal]
        
    '''
    Checks if current choice branch has a next value.
    Return wheter if its True or not.
    '''
    def hasNextVal(self):
        nextValExists = self.currentVal < len(self.getVals) - 1
        return nextValExists


    '''
    Yields all values of a choice branch.
    '''
    def yieldVal(self):
        for c in self.nodes:   
            if c.token.type == TokenTypes.CHOICE:
                yield c.yieldVal()
            else: yield c

class DotDotNode(BaseNode):
    def __init__(self, token:Token, start:BaseNode, end:BaseNode) -> None:
        super().__init__(token)
        self.start = start
        self.end = end

    def visit(self, symboltable: SymbolTable):
        startNode = self.start(symboltable)
        if startNode.token.type != TokenTypes.INTEGER:
            return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))
        
        endNode = self.end(symboltable)
        if endNode.token.type != TokenTypes.INTEGER:
            return FailNode(Token(TokenTypes.FAIL, TokenTypes.FAIL.value))
        
        fac = 1
        if startNode.value > endNode.value:
            fac = -1

        nodes = []
        nodes.append(startNode.value)

        currentInt = startNode.value
        endGen = False

        while endGen == False:
            if currentInt == endNode.value:
                endGen == True
            else:
                currentInt += fac
                nodes.append(currentInt)
           
        return ChoiceSequenceNode(Token(TokenTypes.CHOICE,TokenTypes.CHOICE.value), nodes)

'''
Fail node indicating false? in Verse.
'''
class FailNode(BaseNode): # Technically not need, since Fail node is 1 to 1 a BaseNode
    def __init__(self, token:Token) -> None:
        super().__init__(token)
    
    def __repr__(self) -> str:    
        return self.token.value 

    def visit(self, symboltable: SymbolTable):
        return self 