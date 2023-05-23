from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter
import start_text

"""
TUPLE
"""
# text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)" # ((7,7,31)|(7,7,5)|(7,22,31)|(7,22,5))
text = "x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)" # ((1,1)|(3,3)|(2,1)|(2,3))
# text = "for(x:=10|20; x>10; y:=1|2|3; y<3)do(x+y)"


"""
FOR
"""
# text = "for{1..10}" # (1,2,3,4,5,6,7,8,9,10)
# text = "for{3|4}" # (3,4)
# text = "for{false?}" # ()
# text = "for(x:=10|20; x>10; y:=1|2|3; y<3)do(x+y)" # (21|22) <- filtering variables
# text = "for(x:=10|20; y:=1|2|3)do(x+y)" # (11|12|13|21|22|23)
# text = "for(x:=2|3|5)do(x+1)" # (3|4|6)
# text = "for(x:=10|20) do (x | x+1)" # ((10|20)|(11|21))
# text = "for(x:=2|3|5; x > 2)do(x+(1|2))" # (4|5|6|7)
# text = "t:=(1,1,1); for(i:int;x:=t[i]) do (x+i)" # !!!!!!!! indexing for still work in progress
# text = "t:=(1,2,3); for(i:int;x:=t[1]) do (x)"

"""
IF
"""
# text = "x:int; x=10; if(x=r:int) then 70 else 30" #!!!!!!! # 30
#text = "x,y:int; if(x<20) then y=70 else y=10; x=7; y" # 70
# text = "x,y:int; y = (if (x = 0) then 3 else 4); x = 7; y" # 4
#text = "x; x = 10; r=11; if(x = r:int) then (x:int; 1) else 3" # !!!!!!! SOLL NICHT FUNKTIONIEREN, WEIL ER ERST SCOPED IM THEN ODER ELSE, ALSO SOLLTE ES GLAUB ICH PASSEN
text = "x:int; x=10; y:=(if(x=r:int) then 70 else 30); r=10; y" # 70
#text = "x,y,p,q:int; if(x=0) then {p=3;q=4} else {p=333;q=444}; x=0; (p,q)" # (3,4)
#text = "x,y,p,q,r:int; if(x=0) then {p = r; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)" # (10,4)
#text = "x,y,p,q:int; if(x=0) then { p = r:int; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)" # (10,4)
#text = "x,y,p,q:int; if(x=0) then { p = r; r=10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)" # (10,4)
# text = "if(i:=(15|2|3)) then i else 30"
# text = "i:=(1|2|3); r:=(4|5|6); t:=0; if(t=0) then (i + r) else (r - i)"
# text = "if(i:=1|2|3; r:= 4|5|6) then i + r else r - i"

"""
FUNCTION
"""
# text = "x:int; z:int; f(p:int,q:int):int :=  (p = 1; q = 23; y:int; y = 100; (p+q)*100); f(x,z); x + z" # 
# text = "x:int; f(p:int):int :=  (p = 1; y:int; y = 100; (p)*100); f(x); x" #  
text = "f:=(x:int=> d(x) + 1 ); d(p:int):= (p*2); f(3)" # 7

"""
CHOICE
"""
# text = "1..10" # (1|2|3|4|5|6|7|8|9|10)
# text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)" # ((7,7,31)|(7,7,5)|(7,22,31)|(7,22,5))
# text = "x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)" # (((1,1)|(3,3)|(2,1)|(2,3))
# text = "t:=(10,27,32); x:=(1 | 0 | 1); t[x]" # (27,10,27)
# text = "x:=10|20|15; x<20" # (10|15)
# text = "x,y:int; y = 31|5; x = 7|22; (x,y)" # ((7,31)|(7,5)|(22,31)|(22,5))
# text = "x,y:int; x = 7|22; y = 31|5; (x,y)" # !!!!!!!!
# text = "x:int; t:=(1,(1|(2;3;x)));x = 10; t" # ((1,1)|(1,10))

"""
UNIFICATION
"""
text = "x:int; x=23; x = 23;  x" # 23
text = "x,y,p,q:int; if(x=0) then { p = r; r=10; p=11; r:int; q=4} else {p=333;q=444}; x=0; (p,q)" # FALSE
text = "x:int; x = (z:int,2); x = (3,y:int,r:int); x" # FALSE
text = "x:int; x = (z:int,2); x = (3,y:int); x" # (3,2)
text = "x:int; x=23; x = 2;  x" # FALSE
text = "z:=x+y; x,y:int; x=7; y = 3;z" # 10
text = "x:=1; y:=2; z:int; z = x; z = y; z" # false?
text = "x:int; x=\"Hello \";x" # false?, no unification defined
text = "x,y,p,q:int; if(x=0) then { p = r; r=10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)"

"""
FALSE
"""
#text = "x:int; x:int; r=11; r:int; r" # FALSE
#text = "x:=10; x<7; 3" #FALSE
#text = "x,y:int; y= 4; x=y" # 4
#text = "x:int; x=7; x=3" # FALSE
#text = "x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)" # Disregards z due to context
# text = "x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)" # Disregards z due to context
#text = "for(x:=10|20) do (x | x+1)"
#text = "x:int; (x=3; x+1)|(x=4; x+4)" # (4|8)
# text = "x:int; x:int; r=11; r:int; r" # FALSE
# text = "x:=10; x<7; 3" #FALSE
# text = "x,y:int; y= 4; x=y" # FALSE
# text = "x:int; x=7; x=3" # FALSE
#text = "z:int; x=(y|2); y=(1|3|z); x,y:int; t:int; t = (z = 10; 2); (x,y)" # ((1,1)|(3,3)|(10,10)|(2,1)|(2,3)|(2,10))
# text= "for(x,y:int; x = (10|20); y = (1|2|3))do(false?)"
# text = "z:int; x=(y|2); y=(1|3|z); x,y:int; t:int; t = (z = 10; 2); (x,y)" # ((1,1)|(3,3)|(10,10)|(2,1)|(2,3)|(2,10))

# text = "x:int;a:int; x=2; (x:int => (x:int => (x:int => x + 2) (x)) (x)) (x)"
# text = "y=3; (x:int => 2 + x) (y:int)"
# text = "f(x:int):int := x+1; f(3)"

"""
STRING
"""
# text = "x:=\"Hello \"; y:=\"World\"; x + y" # Hello World
# text = "x:=\"World\"; y:=\"World\"; if(x=y)then 1 else 0" # 1
# text = "x:=\"df\"; y:=\"World\"; x<y" # df
# text = "x:=\"OMGODF\"; y:=\"World\"; x>=y" # OMGODF
# text = "x:=\"df\"; y:=\"World\"; x>=y" # false?
# text = "x:=(\"Hallo\" | \"Welt\" ); x" # (Hallo|Welt)
# text = "x:=(\"Hallo\" | \"Welt\" ); y:=(\"New\" | \"Old\" ); x + y" # (HalloNew|HalloOld|WeltNew|WeltOld)

"""
DATA TYPES
"""
# text = "data Rectangle(width:int,height:int); rec := Rectangle(7,3); rec.width | rec.height"
# # text = "z:int; z=7; y:=(31|5); x:=(7|22); data TupleCombiner(tuples:int); result := TupleCombiner((z,x,y)); result.tuples"
# text = "data Structure(property:int); s := Structure(x); x=5; x:int; s.property"


start_text
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))