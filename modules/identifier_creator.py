from random import randrange
from symboltable import SymbolTable


class IdentifierCreator:

      
    def create(symboltable:SymbolTable):
        return IdentifierCreator.get(symboltable,"")
    
    def get(symboltable:SymbolTable, startingChar:str):
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        id = randrange(100)
        for alph in alphabet:
            newIdentifier = startingChar + alph + str(id)

            if(symboltable.check_if_exists(newIdentifier) == False):
                return newIdentifier
         
        return IdentifierCreator.get(symboltable,startingChar + "var")