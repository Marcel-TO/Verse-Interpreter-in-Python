from syntaxtree.nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter

# --HIER GEÄNDERT
# Beispiel Verse Programme
text = "if(\"a\"= \"a\") then 0 else 1" # Ist-Gleich
text = "\"hallo 123\""  # Nur text
text = "\"123\" > \"§23\"" # Kleiner Zeichen (Wie in Python)
text = "\"123\" < \"§23\"" # Größer Zeichen (Wie in Python)
text = "\"123\" >= \"§23\"" # Größer Gleich Zeichen (Wie in Python)
text = "\"123\" <= \"§23\"" # Kleiner Gleich Zeichen (Wie in Python)
text="ac:string; ac = \"a\"; ac + \"a\"" # Mit typ string auf Variable. Kann sein, das hier es nicht bei allen testcases korrekt funktioniert
text = "\"123\" * \" §23\""
lexer = lexicon(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
print(repr(result))