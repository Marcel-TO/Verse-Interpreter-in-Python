from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter


text = "x:int; z:int; f(p:int,q:int):int :=  (p = 1; q = 23; y:int; y = 100; (p+q)*100); f(x,z); x + z"
text = "x,y:int; if(x<20) then y=70 else y=10; x=7; y"
# text = "1..4"

text = "x,y:int; if(x<20) then y=70 else y=10; x=7; y" #!!!! x=7 reverse
# text = "x,y:int; y = (if (x = 0) then 3 else 4); x = 7; y"
text = "x,y,p,q,r:int; if(x=0) then {p = r; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)"
#text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)"
text = "x,y,p,q:int; if(x=0) then {p=3;q=4} else {p=333;q=444}; x=0; (p,q)"
text = "x,y,p,q:int; if(x=0) then { p = r; r = 10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)"
# text = "z:=x+y; x,y:int; x=7; y = 3;z"
# text = "for{1..10}" # !!!!!
# text = "for{3|4}"
# text = "for{false?}"
# text = "for{i:int; i=3; i<7}" 
# text = "1..10" # CHOICE
# text = "p:int; p=r; p"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))