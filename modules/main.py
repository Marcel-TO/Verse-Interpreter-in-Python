from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter


text = "x:=(y|2); y:=(7|8); (x,y)"
text = "z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)"
text = "x:int; x=7; if(x<20) then x else 333"
text = "z:=x+y; x,y:int; x=7; y = 3;z"
text = "for{1..10}"
text = "for{3|4}"
text = "for{false?}"
text = "for{i:int; i=3; i<7}"
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))