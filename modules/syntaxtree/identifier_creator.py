class IdentifierCreator:

      
    def create(existing):
        return IdentifierCreator.get(existing,"")
    
    def get(existing, startingChar):
        alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
        for alph in alphabet:
            startingChar = startingChar + alph
            exists = False
            index = 0
            maxIndex = len(existing)

            while (exists == False and index < maxIndex):
                if alph == existing[index]:
                    exists = True
                index += 1
            if exists == False:
                return alph
        return IdentifierCreator.get(existing,startingChar + "var")