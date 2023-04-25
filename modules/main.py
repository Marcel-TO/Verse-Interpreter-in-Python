from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter


text = "f(p:int,q:int):int :=  p + q; f(1,2)"
text = "x:int; f(p:int,q:int):int := (p=32; p + q); f(x,2); x"
# text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)"
# text = "x:int; if(x<20) then x else 333; x=7; x" #!!!! x=7 reverse
# text = "z:=x+y; x,y:int; x=7; y = 3;z"
# text = "for{1..10}" # !!!!!
# text = "for{3|4}"
# text = "for{false?}"
# text = "for{i:int; i=3; i<7}" 
# text = "1..10" # CHOICE
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))