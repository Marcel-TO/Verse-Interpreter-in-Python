import string
import unittest

from ddt import ddt, data, unpack
from nodes import *
from verse_lexer import lexicon
from verse_parser import Parser
from verse_interpreter import Interpreter

@ddt
class InterpreterTest(unittest.TestCase):
    '''
    Test: Tuple
    '''
    @data({'input': 'z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)', 'expected': '((7,7,31)|(7,22,31)|(7,7,5)|(7,22,5))'},
          {'input': 'x:=(y|2); y:=(7|8); (x,y)', 'expected': '((7,7)|(8,8)|(2,7)|(2,8))'},
          {'input': 'x:=(1,23,13); x[0..4]', 'expected': '(1|23|13)'},
          {'input': 'x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)', 'expected': '((10,10)|(2,10))'})
    @unpack
    def test_tuple(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)
    
    @data({'input': 'ys:= (12,22,23); xs:= (1,2,3,4); for{((i:int;ys[i])|(s:int; xs[s]))}', 'expected': '(12,22,23,1,2,3,4)'}, # append
    {'input': 'xs:= (1,2,3,4); for{i:int; i > 0; xs[i]}', 'expected': '(2,3,4)'}, # tail
    # {'input': 't:=for{1|2}; t[0]', 'expected': '1'}, # head
    {'input': 'i:int; x:=1; xs:= (2,3,4); for{x|xs[i]}', 'expected': '(1,2,3,4)'}, # cons
    {'input': 'xs:=(1,2,3); f:=(x:int => x * 2); for{i:int;f(xs[i])}', 'expected': '(2,4,6)'}, # flatMap
    {'input': 'xs:=(1,2,3); ys:=(4,5,6); for{i:int; (xs[i], ys[i])}', 'expected': '((1,4),(2,5),(3,6))'},) # zipWith
    @unpack
    def test_functions_on_tuples(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

    '''
    Test: FOR
    '''
    @data({'input': 'for{1..10}', 'expected': '(1,2,3,4,5,6,7,8,9,10)'},
    {'input': 'for{3|4}', 'expected': '(3,4)'},
    {'input': 'for{false?}', 'expected': '()'},
    {'input': 'for(x:=10|20; x>10; y:=1|2|3; y<3)do(x+y)', 'expected': '(21,22)'}, # <- filtering variables
    {'input': 'for(x:=10|20; y:=1|2|3)do(x+y)', 'expected': '(11,12,13,21,22,23)'},
    {'input': 'for(x:=2|3|5)do(x+1)', 'expected': '(3,4,6)'},
    {'input': 't:=(1,1,1); for(i:int;x:=t[i]) do (x+i)', 'expected': '(1,2,3)'}, # <- indexing still work in progress
    {'input': 't:=(1,2,3); for(i:int;x:=t[1]) do (x)', 'expected': '(2)'},
    {'input': 'ys:= (12,22,23); xs:= (1,2,3,4); for{((i:int;ys[i])|(s:int; xs[s]))}', 'expected': '(12,22,23,1,2,3,4)'}, # append
    {'input': 'xs:= (1,2,3,4); for{i:int; i > 0; xs[i]}', 'expected': '(2,3,4)'}, # tail
    {'input': 't:=for{1|2}; t[0]', 'expected': '1'}, # head
    {'input': 'ys:= (1,2); xs:= (3,4); for{a=2; i:int; (xs[i], ys[i], a:int)}', 'expected': '((3,1,2),(4,2,2))'},
    {'input': 'for{i=2;z=20;(i:int)..(z:int)}', 'expected': '(2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20)'},
    {'input': 'for(x:=2|3|5; x > 2)do(x+(1|2))', 'expected': '((4,6)|(4,7)|(5,6)|(5,7))'},
    {'input': 'for(x:=10|20) do (x | x+1)', 'expected': '((10,20)|(10,21)|(11,20)|(11,21))'},)
    @unpack
    def test_for(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)
    
    '''
    Test: IF
    '''
    @data({'input': 'x:int; x=10; if(x=r:int) then 70 else 30', 'expected': '30'},
    {'input': 'x:int; x=10|0; if(x=0) then 70 else 30', 'expected': '(30|70)'},
    {'input': 'x,y:int; if(x<20) then y=70 else y=10; x=7; y', 'expected': '70'},
    {'input': 'x,y:int; y = (if (x = 0) then 3 else 4); x = 7; y', 'expected': '4'},
    {'input': 'x; x = 10; r=11; if(x = r:int) then (x:int; 1) else 3', 'expected': 'false?'},
    {'input': 'if(i:=(15|2|3)) then i else 30', 'expected': '15'},
    {'input': 'if(i:=1|2|3; r:= 4|5|6) then i + r else r - i', 'expected': '5'},
    {'input': 'x,y,p,q,r:int; if(x=0) then {p = r; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)', 'expected': '(10,4)'},
    {'input': 'x,y,p,q:int; if(x=0) then { p = r:int; r = 10; q=4} else {p=333;q=444}; x=0; (p,q)', 'expected': '(10,4)'},
    {'input': 'x,y,p,q:int; if(x=0) then { p = r; r=10; r:int; q=4} else {p=333;q=444}; x=0; (p,q)', 'expected': '(10,4)'},
    {'input': 'x,y,p,q:int; if(x=0) then {p=3;q=4} else {p=333;q=444}; x=0; (p,q)', 'expected': '(3,4)'},)
    @unpack
    def test_if(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

    '''
    Test: FUNCTION
    '''    
    @data({'input': 'x:=1; f(x:int):int := (x + 1)', 'expected': '2'},
    {'input': 'x:int; f(p:int):int :=  (p = 1; y:int; y = 100; (p)*100); f(x); x', 'expected': '1'},
    {'input': 'f:=(x:int=> d(x) + 1 ); d(p:int):= (p*2); f(3)', 'expected': '7'},
    {'input': 'f:=(x:int=> d(x) + 1 ); d(p:int):= (p*2); f(3|2)', 'expected': '(7|5)'},
    {'input': 'f:= (x:int => x + 2); f(23) * 2', 'expected': '50'},
    {'input': 'a=2; f:= (a:int => a + 2);  f(2) * 2; a:int', 'expected': '2'},
    {'input': 'adding:=(xs:int, y:int => 6 + xs + y); adding(1|2,33|44) + (23 | 22)', 'expected': '(63|62|74|73|64|63|75|74)'},
    {'input': 'adding:=(xs:int, y:int => 6 + xs + y); adding(1|2,33|44) + 23 | 22', 'expected': '((63|74)|(64|75)|22)'},
    {'input': 'x:int; z:int; f(p:int,q:int):int :=  (p = 1; q = 23; y:int; y = 100; (p+q)*100); f(x,z); x + z', 'expected': '24'},)
    @unpack
    def test_function(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

    '''
    Test: CHOICE
    '''
    @data({'input': '1..10', 'expected': '(1|2|3|4|5|6|7|8|9|10)'},
    {'input': 'z:int; z=7; y:=(31|5); x:=(7|22); (z,x,y)', 'expected': '((7,7,31)|(7,22,31)|(7,7,5)|(7,22,5))'},
    {'input': 'x=(y|2); y=(1|3|z:int); x,y:int; t:int; t = (z = 10; 2); (x,y)', 'expected': '((10,10)|(2,10))'},
    {'input': 't:=(10,27,32); x:=(1 | 0 | 1); t[x]', 'expected': '(27|10|27)'},
    {'input': 'x,y:int; y = 31|5; x = 7|22; (x,y)', 'expected': '((7,31)|(22,31)|(7,5)|(22,5))'},
    {'input': 'x,y:int; x = 7|22; y = 31|5; (x,y)', 'expected': '((7,31)|(7,5)|(22,31)|(22,5))'},
    {'input': 'x:int; t:=(1,(1|(2;3;x)));x = 10; t', 'expected': '((1,1)|(1,10))'},
    {'input': 'x:=10|20|15; x<20', 'expected': '(10|15)'})
    @unpack
    def test_choice(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

    '''
    Test: UNIFICATION
    '''    
    @data({'input': 'x:int; x=23; x = 23;  x', 'expected': '23'},
    # {'input': 'x,y,p,q:int; if(x=0) then { p = r; r=10; p=11; r:int; q=4} else {p=333;q=444}; x=0; (p,q)', 'expected': 'false?'},
    {'input': 'x:int; x = (z:int,2); x = (3,y:int,r:int); x', 'expected': 'false?'},
    {'input': 'x:int; x = (z:int,2); x = (3,y:int); x', 'expected': '(3,2)'},
    {'input': 'x:int; x=23; x = 2;  x', 'expected': 'false?'},
    {'input': 'z:=x+y; x,y:int; x=7; y = 3;z', 'expected': '10'})
    @unpack
    def test_unification(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

    '''
    Test: FALSE
    '''    
    @data({'input': 'x:int; x:int; r=11; r:int; r', 'expected': 'false?'},
    {'input': 'x:=10; x<7; 3', 'expected': 'false?'},
    {'input': 'x,y:int; x=7; y=4; x=y', 'expected': 'false?'},
    {'input': 'x:int; x="Hallo"', 'expected': 'false?'},
    {'input': 'x:string; x=1', 'expected': 'false?'},
    {'input': 'x:int; x=7; x=3', 'expected': 'false?'})
    @unpack
    def test_false(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)
    
    '''
    Test: STRING
    '''    
    @data({'input': 'x:="Hello "; y:="World"; x + y', 'expected': 'Hello World'},
    {'input': 'x:="World"; y:="World"; if(x=y)then 1 else 0', 'expected': '1'},
    {'input': 'x:="df"; y:="World"; x<y', 'expected': 'df'},
    {'input': 'x:="OMGODF"; y:="World"; x>=y', 'expected': 'OMGODF'},
    {'input': 'x:="df"; y:="World"; x>=y', 'expected': 'false?'},
    {'input': 'x:int; x="Hello"; x', 'expected': 'false?'},
    {'input': 'x:=("Hallo" | "Welt" ); x', 'expected': '(Hallo|Welt)'},
    {'input': 'x:=("Hallo" | "Welt" ); y:=("New" | "Old" ); x + y', 'expected': '(HalloNew|HalloOld|WeltNew|WeltOld)'})
    @unpack
    def test_string(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)
    
    '''
    Test: DATA STRUCTURE
    '''    
    @data({'input': 'data Rectangle(width:int,height:int); rec := Rectangle(7,3); rec.width | rec.height', 'expected': '(7|3)'},
    # {'input': 'data Rectangle(width:int,height:int); rec := Rectangle(7,3); rec = rec', 'expected': '(7|3)'},
    {'input': 'data Rectangle(width:int,height:int); rec := Rectangle(7|1,3|4); (rec.width,rec.height)', 'expected': '((7,3)|(7,4)|(1,3)|(1,4))'},
    {'input': 'data Rectangle(width:int,height:int); rec := Rectangle(7|1,3); recTwo := Rectangle(2|5,8); (rec.width,recTwo.width)', 'expected': '((7,2)|(7,5)|(1,2)|(1,5))'},
    {'input': 'z:int; z=7; y:=(31|5); x:=(7|22); data TupleCombiner(tuples:int); result := TupleCombiner((z,x,y)); result.tuples', 'expected': '((7,7,31)|(7,22,31)|(7,7,5)|(7,22,5))'},
    {'input': 'data MixedRectangle(width:int,height:int,name:string); rec := MixedRectangle(5,4,"AwesomeRectangle"); rec.name|rec.width|rec.height', 'expected': '(AwesomeRectangle|5|4)'},
    {'input': 'data Structure(property:int); s := Structure(x); x=5; x:int; s.property', 'expected': '5'},
    {'input': 'data Rectangle(width:int,height:int); rec := Rectangle(7,3); rec', 'expected': '(7,3)'})
    @unpack
    def test_data(self, input: string, expected: string):
        self.lexer = lexicon(input)
        self.parser = Parser(self.lexer)
        self.interpreter = Interpreter(self.parser)
        result = self.interpreter.interpret()
        self.assertTrue(repr(result) == expected)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)       