import copy
from tokenTypes import TokenTypes

'''
Creates a/or many possible sequences.
''' 
class Sequentor:
    '''
    Gets the nodes to find possible seqences.
    '''
    def __init__(self, nodes:list) -> None:
        self.nodes = nodes
        self.others = []
        self.choices = []
        self.references = []
        self.pointer_pos = 0


    '''
    Gets the resulting seqeunces.
    '''
    def getSequences(self):
        self.setUpNodes()
        sequences = self.createSequences() 
        return sequences 

    '''
    Sets up the nodes of the sequences by differenciating choices and other values (Integers, Tuple).
    As well coping each to their own list, which will be combined later on.
    Row need to be saved and the node wihin the seqeunce to know where the reuslting value
    of a node needs to be stored in a new/resulting list.
    '''
    def setUpNodes(self):
        row = 0
        
        for n in self.nodes:
            if n.token.type == TokenTypes.CHOICE:

            # Deep copy since duplicates can change value during operation of functions.
            # y:=(31|5); x:=(7|22); ((2|3),x,y)
                self.choices.append([row, copy.deepcopy(n)]) 

            else: self.others.append([row, n])
            row += 1


    '''
    Sets up the list with values that are fix (Not choices):
    Example: (( 31 | 4 ), 9, (23,77))
    cv_fix -> [0, 1, 2]
    *Raplace values with the right ones (Fixed values only for now)*
     cv_fix -> [0, 9, (23,77)]
    '''
    def setUp(self):
        cv_fix = list(range(0, len(self.choices) + len(self.others)))
        for o in self.others:
            cv_fix[o[0]] = o[1]
        return cv_fix
    

    '''
    Creates a list of possible sequenc(es).
    '''
    def createSequences(self):
            # If there are no choices, than return back the nodes given to the sequentor.
            if len(self.choices) == 0:
              return [self.nodes]
    
            
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
                    choice_values.append(choiceVals)
                current_index = 0

            return choice_values