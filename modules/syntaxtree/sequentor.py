import copy
from syntaxtree.nodes import *

class Sequentor:
    def __init__(self, nodes:list[BaseNode]) -> None:
        self.nodes:list[BaseNode] = nodes
        self.others = []
        self.choices = []
        self.pointer_pos = 0

    def getSequences(self):
        self.setUpNodes()
        sequences = self.createSequences() 
        return sequences 

    def setUpNodes(self):
        row = 0
        for n in self.nodes:
            node = n.visit(n)
            if node.node.token.type == TokenTypes.CHOICE:
                self.choices.append([row, copy.deepcopy(node.node)]) # Deep copy since duplicates can change value during operation of functions.
            elif node.node.token.type == TokenTypes.FAIL:
                return FailNode(TokenTypes.FAIL, TokenTypes.FAIL.value)
            else: self.choices.append([row, node.node])
            row += 1

   

# Sets up the list with values that are fix (Not choices)
    def setUp(self):
        cv_fix = list(range(0, len(self.choices)))
        for o in self.others:
            cv_fix[o[0]] = o[1]
        return cv_fix

    def createSequences(self):
            current_pointer_pos = len(self.choices) - 2
            last_index = len(self.choices) - 1
            choice_values = []
            current_index = 0
            hasCompleted:bool = False
            point_move_next_choice = False
            hasManyChoices = True

            if(current_pointer_pos < 0):
                current_pointer_pos = 0
                hasManyChoices = False

            while hasCompleted == False:
                choiceVals = self.setUp()
                for c in self.choices:
                
                    current_choice = c[1]

                    if current_index == current_pointer_pos: 
                        if point_move_next_choice :
                            has_next_choice = current_choice.nextChoice()
                            if has_next_choice == False:
                                if current_pointer_pos == 0:
                                    hasCompleted = True
                                    break
                                else: current_pointer_pos -= 1
                            point_move_next_choice = False 
                        val = current_choice.getNextVal(hasManyChoices)
                        
                        # This if statement is only for single choices as such: x:= (2,3); (1,x)
                        if hasManyChoices == False and current_choice.hasNextVal() == False:
                            point_move_next_choice = True

                        choiceVals[c[0]] = val 

                    elif  current_index == last_index:
                        val = None
                        val = current_choice.getNextVal(False)
                        has_next_choice = True
                        if val != None:
                            choiceVals[c[0]] = val
                            
                        if current_choice.hasNextVal() == False:
                            has_next_choice = current_choice.nextChoice()
                        if(has_next_choice == False):
                                point_move_next_choice = True  
                                current_choice.setChoiceBack() 
                    else:
                        val = current_choice.getNextVal(True)    
                        choiceVals[c[0]] = val 

                    current_index += 1
                if(hasCompleted == False):
                    choice_values.append(SequenceNode(Token(TokenTypes.TUPLE_TYPE,TokenTypes.TUPLE_TYPE.value),choiceVals))
                current_index = 0

            return choice_values