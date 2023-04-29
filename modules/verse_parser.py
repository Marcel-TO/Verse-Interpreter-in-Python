from verse_lexer import lexicon
from structure.logger import *
from syntaxtree.nodes import *
from syntaxtree.parsedNode import *
class Parser:
    def __init__(self, lexer: lexicon):
       self.logger: Logger = Console_Logger()
       self.end = False
       self.lexer = lexer
       self.current_token = lexer.get_token(self.lexer.current_char)
       

    def parse(self) -> BaseNode:     
        node = self.program()
        if node.hasSyntaxError or self.current_token.type != TokenTypes.EOF:
            self.logger.__log_error__("it appears there was a problem", ErrorType.SyntaxError)
            return ParsedNode(None, True)
        return node.node
       

    #####################################
    # statements
    #####################################

    """
    Checks if the program has either statements or function calls.
    Rule => statement_list | func_decl (SEMI statement_list | func_decl)*?
    """
    def program(self) -> ParsedNode:
        node = self.block()
        
        # checks if the program is not a function either.
        if(node.hasSyntaxError == True):
            return ParsedNode(None, True)
        
        return ParsedNode(ProgramNode(node.node), False)
    
    

    """
    Checks if the program has a list of statements.
    Rule => statement_list
    """
    def block(self) -> ParsedNode:
        node = self.statement()
        nodes = []
        

        if(node.hasSyntaxError==False):
            nodes.append(node.node)
            # iterates through the input and breaks the block into statements.
            if(self.current_token.type == TokenTypes.SEMICOLON):
                while(self.current_token.type == TokenTypes.SEMICOLON):
                    self.forward()
                    node = self.statement()
                    if node.hasSyntaxError:
                        return ParsedNode(None,True)
                    else: nodes.append(node.node)
                return ParsedNode(BlockNode(nodes), False)
        return node


    """
    Checks if the current node is either an expression statemnts, if statement, for statement, a function call or an assignment statemnt.
    Rule => expr | if | for | func_call | assign_statement
    """
    def statement(self) -> ParsedNode:
        token = self.current_token
        index = self.lexer.index

        node: ParsedNode = self.nested_scope()

        # checks if current node is not a nested scope.
        if(node.hasSyntaxError == True):
            self.set_to_token(index,token)
            node = self.func_decl()

        # checks if current node is not a function declaration.
        if(node.hasSyntaxError == True):
             self.set_to_token(index,token)
             node = self.flexible_eq()

        # checks if current node is not a flexible eq.
        if(node.hasSyntaxError == True):
            self.set_to_token(index,token)
            node = self.expr()

        return node
    

    """
    Flexible Eq Statement (Used only to give something a value)
    Rule -> (Identifier EQUAL expr)
    """
    def flexible_eq(self)-> ParsedNode:
        left_node = self.identifier()
        if(left_node.hasSyntaxError == False):
            if(self.current_token.type == TokenTypes.EQUAL):
                token = self.current_token
                self.forward()
                right_node = self.expr()
                if(right_node.hasSyntaxError == False):
                    return ParsedNode(FlexibleEqNode(token,left_node.node, right_node.node), False)
        return ParsedNode(None,True)


    """
    Rigid Eq Statement (Used only to check if two expr are equals)
    Rule -> (expr (EQUAL expr)*?)
    """
    def rigid_eq(self) -> ParsedNode:
        left_node = self.expr()
        if(left_node.hasSyntaxError == False):
            if(self.current_token.type == TokenTypes.EQUAL):
                node = ParsedNode(None,True)
                while self.current_token.type == TokenTypes.EQUAL:
                    token = self.current_token
                    self.forward()
                    right_node = self.expr()
                    if(right_node.hasSyntaxError == False):
                        if(node.node == None):
                                node = RigidEqNode(token,left_node.node,right_node.node)
                        if(self.current_token.type == TokenTypes.EQUAL):
                            node = RigidEqNode(token, node, right_node)
                    else: return ParsedNode(None,True)
                return ParsedNode(node,False)
            return left_node
        return ParsedNode(None,True)
   
  
    """
    Checks for a function call.
    Rule => IDENTIFIER LB (func_call_args)? RB 
    """
    def func_call(self) -> ParsedNode:
        node = self.identifier()
        if(node.hasSyntaxError):
            return ParsedNode(None, True)  
        if(self.current_token.type == TokenTypes.LBRACKET):
            self.forward()
            
            # checks if it is an empty function call.
            if self.current_token.type == TokenTypes.RBRACKET:
                self.forward()
                return ParsedNode(FuncCallNode(node.node, []), False)

            args = self.func_call_args()
            arg_nodes = []

            for arg in args:
                if arg.hasSyntaxError:
                    return ParsedNode(None, True)
                arg_nodes.append(arg.node)
            if(self.current_token.type == TokenTypes.RBRACKET):
                self.forward()
                return ParsedNode(FuncCallNode(node.node, arg_nodes), False)
                
        return ParsedNode(None, True)
        
    """
    Checks for the arguments of the function call.
    Rule => expr (COMMA expr)*?  
    """    
    def func_call_args(self) -> list[ParsedNode]:
        nodes = []
        nodes.append(self.expr())

        while True:
            if(self.current_token.type == TokenTypes.COMMA):
                self.forward()
                nodes.append(self.expr())
            else:
                for node in nodes:
                    if node.hasSyntaxError:
                        return [ParsedNode(None, True)]
                break
        
        return nodes


    """
    Checks for the declaration of a function.
    Rule => IDENTIFIER LB func_dec_param RB (COLON type)? BINDING block
           |IDENTIFIER BINDING LB nested_scope LAMBDA expr RB    
    """
    def func_decl(self) -> ParsedNode:
        identifier = self.identifier()
        if identifier.hasSyntaxError == False:

            if self.current_token.type == TokenTypes.LBRACKET:
                self.forward()

                params = self.func_decl_param()

                if self.current_token.type == TokenTypes.RBRACKET:
                    self.forward()
                    type = None
                    if(self.current_token.type == TokenTypes.COLON):
                        self.forward()
                        type = self.type()
                        if(type.hasSyntaxError):
                            return ParsedNode(None,True)
                        type = type.node

                    if self.current_token.type == TokenTypes.BINDING:
                        self.forward()
                        block = self.expr()
                        if(block.hasSyntaxError == False):
                            return ParsedNode(FuncDeclNode(identifier.node, params.node, False, type, block.node), False)
                return ParsedNode(None,True)
            
            if self.current_token.type == TokenTypes.BINDING:
                self.forward()
                if self.current_token.type == TokenTypes.LBRACKET:
                    self.forward()
                    type = None
                    params = self.func_decl_param()
                    if(params.hasSyntaxError):
                        return ParsedNode(None,True)
                    
                    if self.current_token.type == TokenTypes.LAMBDA:
                        self.forward()                   
                        block = self.expr()
                        if(block.hasSyntaxError == False and self.current_token.type == TokenTypes.RBRACKET):
                            self.forward()
                            return ParsedNode(FuncDeclNode(identifier.node, params.node, True, type, block.node), False)
                    return ParsedNode(None,True)

        return ParsedNode(None,True)

    """
    Checks for the arguments of the function declaration.
    Rule => nested_scope
    """
    def func_decl_param(self) -> ParsedNode:
        nodes:list[ScopeNode] = []
        if(self.current_token.type == TokenTypes.RBRACKET):
            return ParsedNode(nodes, False)
        
        node = self.scope()
        if(node.hasSyntaxError == False):
            nodes.append(node.node)
            while(self.current_token.type == TokenTypes.COMMA):
                self.forward()
                node = self.scope()
                if(node.hasSyntaxError):
                    return ParsedNode(None, True)
                nodes.append(node.node)
            return ParsedNode(nodes, False)
        return ParsedNode(None, True)


    """
    Checks if the statement is an if statement.
    Rule => IF LB expr RB THEN CBL block CBR ELSE CBL block CBR
          | IF LB expr RB THEN expr ELSE expr  
    """
    def if_statement(self) -> ParsedNode:
        token = self.current_token

        if token.type != TokenTypes.IF:
            return ParsedNode(None, True)
        
        self.forward()
        if self.current_token.type != TokenTypes.LBRACKET:
            return ParsedNode(None, True)
        
        self.forward()
        if_node = self.rigid_eq()
        if if_node.hasSyntaxError == True or self.current_token.type != TokenTypes.RBRACKET:
            return ParsedNode(None, True)
        
        self.forward()
        if self.current_token.type != TokenTypes.THEN:
            return ParsedNode(None, True)
        
        self.forward()

        hasCB:bool = self.current_token.type == TokenTypes.CBL
        then_node = ParsedNode(None, True)
        else_node = ParsedNode(None, True)

        if(hasCB):
            self.forward()
            then_node = self.block()
            if(then_node.hasSyntaxError):
                return ParsedNode(None, True)
            if(self.current_token.type == TokenTypes.CBR):
                self.forward()
            else: return ParsedNode(None, True)
        else:
            then_node = self.block()
            if(then_node.hasSyntaxError):
                return ParsedNode(None, True)
            
        if self.current_token.type != TokenTypes.ELSE:
            return ParsedNode(None, True)     
        self.forward()

        if(hasCB):
            if(self.current_token.type == TokenTypes.CBL):
                self.forward()
                else_node = self.block()
                if(else_node.hasSyntaxError):
                    return ParsedNode(None,True)
                if(self.current_token.type == TokenTypes.CBR):
                    self.forward()
                else: return ParsedNode(None,True)
            else: return ParsedNode(None,True)
        else:
            else_node = self.block()
            if(else_node.hasSyntaxError):
                return ParsedNode(None,True)
            
        return ParsedNode(IfNode(token, if_node.node, then_node.node, else_node.node),False)
       

    """
    Checks if the statement is a loop expression.
    Rule => FOR CBL (scope|expr) (;expr)*? CBR
          | FOR LB (scope|expr) (,expr)*? RB DO expr
    """
    def for_loop(self) -> ParsedNode:
        token = self.current_token

        if token.type != TokenTypes.FOR:
            return ParsedNode(None, True)
        
        self.forward()
        # checks if the for loop is defined with a curly bracket.
        if self.current_token.type == TokenTypes.CBL:
            self.forward()
            return self.for_loop_curly()
        elif self.current_token.type == TokenTypes.LBRACKET:
            self.forward()
            return self.for_loop_bracket()

        return ParsedNode(None, True)
            
    
    def for_loop_curly(self) -> ParsedNode:
        condition: ParsedNode
        expression: ParsedNode
        token = self.current_token
        index = self.lexer.index

        node = self.scope()

        # checks if the loop content is not a scope but an expression.
        if node.hasSyntaxError == True:
            self.set_to_token(index, token)
            node = self.expr()
        
        # checks if the loop input is invalid.
        if node.hasSyntaxError:
            return ParsedNode(None, True)
        
        if self.current_token.type == TokenTypes.CBR:
            self.forward()
            return ParsedNode(ForNode(TokenTypes.FOR, node=node.node, condition=None, expr=None, do=None), False)
        
        self.forward()
        token = self.current_token
        index = self.lexer.index
        condition = self.flexible_eq()

        if(condition.hasSyntaxError == True):
            self.set_to_token(index,token)
            condition = self.expr()

        if condition.hasSyntaxError:
            return ParsedNode(None, True)

        if self.current_token.type == TokenTypes.SEMICOLON:
            self.forward()
            token = self.current_token
            index = self.lexer.index
            expression = self.flexible_eq()

            if(expression.hasSyntaxError == True):
                self.set_to_token(index,token)
                expression = self.expr()
        
            if self.current_token.type != TokenTypes.CBR or expression.hasSyntaxError:
                return ParsedNode(None, True)

            self.forward()
            return ParsedNode(ForNode(TokenTypes.FOR, node=node.node, condition=condition.node, expr=expression.node, do=None),False)
        
        if self.current_token.type == TokenTypes.CBR:
            self.forward()
            return ParsedNode(ForNode(TokenTypes.FOR, node=node.node, condition=None, expr=condition.node, do=None), False)
        
        return ParsedNode(None, True)
    
    def for_loop_bracket(self) -> ParsedNode:
        condition: ParsedNode
        expression: ParsedNode
        token = self.current_token
        index = self.lexer.index

        node = self.scope()

        # checks if the loop content is not a scope but an expression.
        if node.hasSyntaxError == True:
            self.set_to_token(index,token)
            node = self.expr()
        
        # checks if the loop input is invalid.
        if node.hasSyntaxError:
            return ParsedNode(None, True)
        
        if self.current_token == TokenTypes.RBRACKET:
            self.forward()
            return ParsedNode(ForNode(TokenTypes.FOR, node=node.node, condition=None, expr=None, do=None), False)
        
        self.forward()
        token = self.current_token
        index = self.lexer.index
        condition = self.flexible_eq()

        if(condition.hasSyntaxError == True):
            self.set_to_token(index,token)
            condition = self.expr()

        if condition.hasSyntaxError:
            return ParsedNode(None, True)

        if self.current_token.type == TokenTypes.SEMICOLON:
            self.forward()
            token = self.current_token
            index = self.lexer.index
            expression = self.flexible_eq()

            if(expression.hasSyntaxError == True):
                self.set_to_token(index,token)
                expression = self.expr()
        
            if self.current_token.type != TokenTypes.RBRACKET or expression.hasSyntaxError:
                return ParsedNode(None, True)
        
            self.forward()
            if self.current_token.type != TokenTypes.DO:
                return ParsedNode(None, True)
        
            self.forward()
            do = self.expr()
        
            if do.hasSyntaxError:
                return ParsedNode(None, True)
            
            return ParsedNode(ForNode(token, node=node.node, condition=condition.node, expr=expression.node, do=do.node), False)
        
        if self.current_token.type != TokenTypes.RBRACKET:
                return ParsedNode(None, True)
        
        self.forward()
        if self.current_token.type != TokenTypes.DO:
            return ParsedNode(None, True)
        
        self.forward()
        do = self.expr()
        
        if do.hasSyntaxError:
            return ParsedNode(None, True)
            
        return ParsedNode(ForNode(token, node=node.node, condition=None, expr=condition.node, do=do.node), False)


    """
    Checks if the statement is a nested scope.
    Rule =>  (Identifier COMMA Identifier)* COLON TYPE
    """
    def nested_scope(self) -> ParsedNode:
        nodes: list[ParsedNode] = []
        nodes.append(self.identifier())
        scope_nodes = []

        if nodes[0].hasSyntaxError:
            return ParsedNode(None, True)
            
        hasComma:bool = False
        while True:        
            if self.current_token.type == TokenTypes.COMMA:
                hasComma = True
                self.forward()
                nodes.append(self.identifier())
                
            else:
                for node in nodes:
                    if node.hasSyntaxError:
                        return ParsedNode(None, True)
                    scope_nodes.append(node.node)
                break
        
        if hasComma == False or self.current_token.type != TokenTypes.COLON:
            return ParsedNode(None, True)
        token = self.current_token
        self.forward()
        type = self.type()

        if type.hasSyntaxError == True:
            return ParsedNode(None, True)

        return ParsedNode(ScopeNode(token, scope_nodes, type.node), False)
        
        
    #####################################
    # expressions
    #####################################

    def expr(self) -> ParsedNode:         
        startNode = self.choice()

        if startNode.hasSyntaxError:
            return ParsedNode(None, True)

        if self.current_token.type == TokenTypes.DOTDOT:
            token = self.current_token
            self.forward()
            endNode = self.choice()

            if endNode.hasSyntaxError:
                return ParsedNode(None, True)
            
            return  ParsedNode(DotDotNode(token, startNode.node, endNode.node),False)
        
        return startNode  
        
        
        

        

    
    def choice(self):
        node = self.operation()
        token = self.current_token

        nodes:list[BaseNode] = []
     
        if(node.hasSyntaxError==False and self.current_token.type == TokenTypes.CHOICE):
                nodes.append(node.node)
                while(self.current_token.type == TokenTypes.CHOICE):
                    token = self.current_token
                    self.forward()
                    node = self.operation()
                    if(node.hasSyntaxError==False):
                        nodes.append(node.node)
                    else: return ParsedNode(None, True)
                return ParsedNode(ChoiceSequenceNode(token, nodes), False)
        return node
    

    """
    This method checks if a token any of the following operations: =, <, >, <=, >=, |, +, -
    Since all of this operations have the same priority and same values output, it is not needed to write them in different methods
    """
    def operation(self):
        # RULE --> op: term ((GT|LT|GE|LE|EQUAL|CHOICE|PLUS|MINUS) term)*
        left_node = self.term()

        # Checks if left node has been received and if the following token is one of the following tokens: : =, <, >, <=, >=, |, +, -
        if(left_node.hasSyntaxError == False and (self.check_type(self.current_token.type,
                [TokenTypes.GREATER,TokenTypes.GREATEREQ,TokenTypes.LOWER,TokenTypes.LOWEREQ, TokenTypes.PLUS,
                TokenTypes.MINUS]))):

                node = ParsedNode(None,True)
                
                # The while method "concatenates" the operations
                while(self.check_type(self.current_token.type,
                [TokenTypes.GREATER,TokenTypes.GREATEREQ,TokenTypes.LOWER,TokenTypes.LOWEREQ, TokenTypes.PLUS,
                TokenTypes.MINUS])):
                
                    token = self.current_token
                    self.forward()
                    right_node = self.term()
                    if(right_node.hasSyntaxError):
                        return right_node
                    
                    # Binds found operation to its left node
                    if(node.node == None):
                       node = ParsedNode(OperatorNode(token, left_node.node, right_node.node),False)
                    else: node = ParsedNode(OperatorNode(token, node.node, right_node.node),False)
                return node
        return left_node


    """
    Checks the same way in operation method but here it checks for *, /
    """
    def term(self) -> ParsedNode:
        # RULE --> factor ((MUL|DIV) factor)*
        left_node = self.factor() 

        if(left_node.hasSyntaxError == False and (self.check_type(self.current_token.type,[TokenTypes.MULTIPLY, TokenTypes.DIVIDE]))):
            node = ParsedNode(None,True)

             # The while method "concatenates" the operations
            while(self.check_type(self.current_token.type,[TokenTypes.MULTIPLY, TokenTypes.DIVIDE])):
               
                token = self.current_token
                self.forward()
                right_node = self.factor()
                if(right_node.hasSyntaxError):
                    return right_node
                
                # Binds found operation to its left node
                if(node.node == None):
                  node = ParsedNode(OperatorNode(token, left_node.node, right_node.node), False)
                else: node = ParsedNode(OperatorNode(token, node.node, right_node.node), False)
            return node
        return left_node
    

    """
    Checks for unary operations, Integers, brackets (highest priority)
    RULE -->  INTEGER  
        : brackets
        : (MINUS|PLUS) arith
        : func_call x() x
        : indexing     NOT IMPLEMENTING
        : --> means the same as (brackets|unary|func_call) just like in operation()
        only that for each if a different Node may be created not such as only OperationNode like in operation()
    """
    def factor(self) -> ParsedNode:
        token = self.current_token
        index = self.lexer.index

        #Integer check
        if(token.type == TokenTypes.INTEGER):
            self.forward()
            return ParsedNode(NumberNode(token), False)
        
        if(token.type == TokenTypes.FAIL):
            self.forward()
            return ParsedNode(FailNode(token), False)
        
        #Unary operation check
        if(self.check_type(self.current_token.type, [TokenTypes.PLUS, TokenTypes.MINUS])):
            self.forward()
            node = self.factor()
            if(node.hasSyntaxError):        # (--) --> Error needs (-- expr) or (--3)
                return ParsedNode(None, True)
            return ParsedNode(UnaryNode(token, node.node), False)
        
        #brackets check
        node = self.brackets()

        #if node has failed check for loop
        if(node.hasSyntaxError):
            self.set_to_token(index, token)
            node = self.indexing()

        #if node has failed check for loop
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.scope()

         #if node has failed check for loop
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.binding()

        #if node has failed check indexing
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.func_call()
        
        #if node has failed check for loop
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.for_loop()

        #if node has failed check if statement
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.if_statement()
        
        #if node has failed check sequence
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.sequence()
        
        #if node has failed check identifier
        if(node.hasSyntaxError):
            self.set_to_token(index,token)
            node = self.identifier()
        return node
    

    """
    Checks for brackets (highest priority)
    RULE --> brackets: LB expr RB
    """
    def brackets(self) -> ParsedNode: 
        if(self.current_token.type == TokenTypes.LBRACKET):
            self.forward()
            node = self.block()
        
            if(self.current_token.type == TokenTypes.RBRACKET):
                self.forward()
                return node
        return ParsedNode(None,True)
        

    """
    y := 8 y:=(x:int)  y:= method(...)...
    RULE --> scope BINDING expr
    """
    def binding(self) -> ParsedNode:
        left_node = self.identifier()

        if(left_node.hasSyntaxError == False):
            if(self.check_type(self.current_token.type,[TokenTypes.BINDING])):
                token = self.current_token
                self.forward()
                right_node = self.expr()
                if(right_node.hasSyntaxError == False):
                    return ParsedNode(BindingNode(token, left_node.node, right_node.node), False)
                else: return ParsedNode(None,True)
        return ParsedNode(None,True)


    """
    x:int
    RULE --> identifier COLON type 
    """
    def scope(self) -> ParsedNode:
        left_node = self.identifier()
        if(left_node.hasSyntaxError == False):
            if(self.check_type(self.current_token.type, [TokenTypes.COLON])):
                token = self.current_token
                self.forward()
                type = self.type()
                if(type.hasSyntaxError == False):
                    return ParsedNode(ScopeNode(token,[left_node.node], type.node), False) # Return Scope Node
                else: return ParsedNode(None, True)
        return ParsedNode(None, True)
    

    """
    variable/method name
    RULE --> identifier
    """
    def identifier(self) -> ParsedNode:
        token = self.current_token
        if(token.type == TokenTypes.IDENTIFIER):
            self.forward()
            return ParsedNode(IdentifierNode(token), False)
        return ParsedNode(None, True) 
        

    """
    int or tuple(int,int) or array{int}
    RULE -->  INT                        
            : TUPLE LB type (,type)* RB 
    """
    def type(self) -> ParsedNode: 
        token = self.current_token
        if(token.type == TokenTypes.INT_TYPE):
            self.forward()
            return ParsedNode(TypeNode(token),False)
        
        if(token.type == TokenTypes.TUPLE_TYPE):
          
            self.forward()
            if(self.current_token.type == TokenTypes.LBRACKET):
                self.forward()
                types:list[TypeNode] = []

                type = self.type()
                if(type.hasSyntaxError == False):
                    types.append(type.node)
                    if(self.check_type(self.current_token.type, [TokenTypes.COMMA])):
                        while(self.current_token.type == TokenTypes.COMMA):

                            self.forward()
                            t = self.type()

                            if(t.hasSyntaxError):  #If on error
                                return ParsedNode(None,True)
                            types.append(t.node) #else append to list of types
                     
            if(self.current_token.type == TokenTypes.RBRACKET):  
                self.forward()
                return ParsedNode(SequenceTypeNode(token, types), False)
            
        return ParsedNode(None, True) 
        

    """
    a[i:int]
    # RULE --> identifier SBL expr SBR
    """
    def indexing(self) -> ParsedNode:
        left_node = self.identifier()
        if(left_node.hasSyntaxError == False):
            if(self.current_token.type == TokenTypes.SBL):
                self.forward()
                expr_node = self.expr()
          
                if(expr_node.hasSyntaxError == False and self.current_token.type == TokenTypes.SBR):
                     self.forward()
                     return ParsedNode(IndexingNode(left_node.node.token, left_node.node, expr_node.node), False)
                return ParsedNode(None,True)
        return ParsedNode(None,True)
    

    """
    RUKE --> LB (expr COMMA expr)* RB                  --> tuple (n1,...)
             array CBL expr (COMMA expr)*? CBR         --> long-form syntax and singleton tuple/array array{n1} oder array{n1,...}
    """
    def sequence(self) -> ParsedNode:
        token = self.current_token
        nodes:list[BaseNode] = []

        # Tuple
        if(token.type == TokenTypes.LBRACKET):
            self.forward()
            node = self.expr()
            if(node.hasSyntaxError==False):
                nodes.append(node.node)
                while(self.current_token.type == TokenTypes.COMMA):
                    self.forward()
                    node = self.expr()
                    if(node.hasSyntaxError==False):
                        nodes.append(node.node)
                    else: return ParsedNode(None,True)
                if(len(nodes) > 1 and self.current_token.type == TokenTypes.RBRACKET):
                    self.forward()
                    return ParsedNode(SequenceNode(Token(TokenTypes.TUPLE_TYPE, TokenTypes.TUPLE_TYPE.value), nodes), False)

        # Array
        if(token.type == TokenTypes.ARRAY_TYPE):
                self.forward()
                if(self.current_token.type == TokenTypes.CBL):
                    self.forward()
                    node = self.expr()
                    if(node.hasSyntaxError == False):
                        nodes.append(node.node)
                        while(self.current_token.type == TokenTypes.COMMA):
                              self.forward()
                              node = self.expr()
                              if(node.hasSyntaxError==False):
                                nodes.append(node.node)
                              else: return ParsedNode(None,True)
                        if(self.current_token.type == TokenTypes.CBR):
                            self.forward()
                            return ParsedNode(SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value), nodes), False)
                        
        return ParsedNode(None, True)
                

    """
    Moves forward in the tokens list
    """
    def forward(self) -> None:
        print(self.current_token.__info__())
        self.lexer.forward()
        self.current_token = self.lexer.get_token(self.lexer.current_char)
        if self.current_token.type == TokenTypes.EOF:
            self.end = True
        

    """
    Checks if a type exists in the following types list
    """
    def check_type(self,type:TokenTypes,types:list[TokenTypes]) -> bool:
        return type in types
    

    """
    Sets current token back if a certain path lead to failure (Wrong syntax)
    May need it for later
    """
    def set_to_token(self,index, token): 
        self.current_token = token
        self.lexer.index = index