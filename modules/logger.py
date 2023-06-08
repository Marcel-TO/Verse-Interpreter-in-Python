from errorClass import ErrorType


class Logger:
    def __init__(self):{}
        
    def __log__(self, string:str):{}

    def __log_error__(self,string:str, type:ErrorType):{}

class Console_Logger(Logger):

    def __log__(self, string:str):
        print(string)

    def __log_error__(self,string:str, type:ErrorType):       
        print("ERROR| " + type.value + ": " + string)