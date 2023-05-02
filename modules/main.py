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
text = "x,y,p,q:int; if(x=0) then { p = r:int; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)"
text = "x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)"
text = "x; x = 10; r=11; if(x = r:int) then x:int; 1 else 3"
text = "x:int; r=11; (1,(1|(2;3;x))) ;x = 10; x"

# text = "x:int; z:int; f(p:int,q:int):int :=  (p = 1; q = 23; y:int; y = 100; (p+q)*100); f(x,z); x + z"
# text = "1..4"
# text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)"
# text = "x,y:int; if(x<20) then y=70 else y=10; x=7; y" #!!!! x=7 reverse
# text = "x,y:int; y = (if (x = 0) then 3 else 4); x = 7; y"
# text = "x,y,p,q:int; if(x=0) then {p=3;q=4} else {p=333;q=444}; x=0; (p,q)"
text = "x,y,p,q:int; if(x=0) then { p = r; r=10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)"
# text = "z:=x+y; x,y:int; x=7; y = 3;z"
text = "for{1..10}" # !!!!!
# text = "for{3|4}"
# text = "for{false?}"
text = "for{i:int; i=3; i<7}" 
# text = "1..10" # CHOICE
# text = "x:int; x=10; if(x=r:int) then 70 else 30"
# text = "for(x:=2|3|5)do(x+1)"
# text = "for(x:=10|20; y:=1|2|3)do(x+y)"
# text = "for(x:=2|3|5; x > 2)do(x+1)"
# text = "x:=10|20|15; x<20"
# text = "x:int; x:int; r=11; r:int; r"
# text = "x:=10; x<7; 3"
# text = "x,y,p,q:int; if(x=0) then { p = r; r = 10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)"
# text = "x,y:int; y= 4; x=y"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))