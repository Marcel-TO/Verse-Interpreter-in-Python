# Verse Interpreter: Exploring the Future of Programming with Python
Welcome to the Verse Interpreter repository! This is a project that showcases an interpreter written in Python for the upcoming Verse programming language. With this interpreter, you can delve into the unique features and capabilities of Verse, experiencing firsthand the potential it holds for the future of programming.

## About Verse
Verse is an upcoming programming language that promises to revolutionize the world of software development. Designed with simplicity, expressiveness, and performance in mind, Verse aims to provide developers with a fresh and powerful tool for crafting elegant and efficient code. With a focus on addressing modern development challenges, Verse offers a unique syntax, extensive standard library, and a range of advanced features to enable developers to build robust and scalable applications across various domains. By combining intuitive syntax with high-performance execution, Verse strives to enhance developer productivity and unlock new possibilities in the realm of programming.

## Verse Source
The development of the Interpreter was driven by a careful selection of reliable and authoritative sources. Extensive research was conducted using language specifications, academic papers and the showcase of Verse in one of the Haskell Exchange conferences.

- [The Verse Calculus: a Core Calculus for Functional LogicProgramming](https://simon.peytonjones.org/assets/pdfs/verse-March23.pdf)
- [Beyond Functional Programming: The Verse Programming Language](https://www.youtube.com/watch?v=832JF1o7Ck8)


## Getting Started
You will need Python installed to run the Verse interpreter. Once set up, you can dive into the project's files and directories to understand the internals of the interpreter and find examples and documentation.

## What Verse Features are covered in the Interpreter?
- Integers​
- Arithmetic Calculations
- Tuples/Arrays​
- Choice​
- Functions​
- If Statements​
- For-loop​
- Unification​
- Strings​
- Own Datatypes

## Implementation of Verse Code
### To bring into Scope
The feature "to bring a variable into scope" in Verse allows for the explicit declaration or assignment of a variable within a specific block or context, making it accessible and usable within that particular scope.
```py
    x:int;
    y,z:int;
```

### Set a Value
It allows the user to declare a value to a specific variable that is already scoped. 
```py
    x:int; x=3
    y=4; y:int; y
```

Which means, if there is a value that is not getting scoped, during the execution, the interpreter will register it as fail and return false?
```py
    x=3
```

### To Bind a Value
With the help of binding, it is possible to scope and set a value at the same time.
```py
    x:=3
```

### Tuples / Array
The main structure of Verse is build around the tuple. It allows for a structured sequence of values inside a single variable.
```py
    x:=(1,2,3,4,5)
```

### Choices
The feature of choices in Verse provides a powerful mechanism for decision-making within the code. It allows to define conditional branches based on different conditions, enabling the execution of specific code blocks based on the evaluation of these conditions.
```py
    x:=(1|2|3)
    x:=(1|2|3); y:=(4|5|6); x + y
```

### Functions
Verse also allows the use of declaring and calling functions like most common programming languages. 
The declaration itself is a bit unique though. To declare a Function it needs to be structured as follows:
```py
    IDENTIFIER(SCOPES):TYPE := (BLOCK)
```
==`Block`==
: A Block stands in Verse for one or multiple expressions.
```py
    f(x:int,y:int):int := (x+y); f(2,3)
```

### If Statements
Every `if` statement in Verse is followed by a `then` and an `else` statement. And besides the `if` both resulting statements can contain a `BLOCK`
```py
    if(EXPRESSION) then EXPRESSION else EXPRESSION
    if(EXPRESSION) then (BLOCK) else (BLOCK)
    if(EXPRESSION) then {BLOCK} else {BLOCK}
```
```py
    if(x>0) then 1 else 0
```

### For loop
The iterator defines a sequence or collection of elements to iterate over, while the loop variable holds the current element of each iteration. The loop body contains the code that is executed repeatedly for each element in the iterator until the iteration is complete. 
```py
    for (BLOCK) do (BLOCK)
```
```py
    for {1..10}  -> (1,2,3,4,5,5,6,7,8,9,10)
    for {3|4}    -> (3,4)
    for {false?} -> ()
```

### String
This feature is not actually presented during the conference, neither is it described in the Verse Calculus. But this interpreter uses the information gathered regarding variables and allows the use of strings.
```py
    x:="Hello World"
    x:=("Hello"|"World")
```

### Own Data Structures
Another feature that is not actually described in the papers, nor talked about in the conferencei is the own data types. Most common programming languages allow the use of custom structures defined and called inside of a program. Take Haskell for example:
```haskell
    data Rectangle = Rectangle
    {
        width :: Int,
        height :: Int
    }
```
Our implementation takes a similar approach and combines the haskell declaration with the Verse function declaration. It is basically a function declaration with a data infront.
```py
    data Rectangle(width:int,height:int); rec := Rectangle(7,3); rec.width | rec.height

    -> (7|3)
```

## Structure
The structure of the interpreter involves multiple components working together to process and execute code.

### Token
Tokens represent reserved characters or strings. These have certain information about what it represents.
Each token has two different values: 
- Name of the token
- Value
![TokenTypes](./pictures/tokentypes.png)

### Lexer
The lexer is the first component in the interpreter structure. 
Its main task is to break the source code into a set of tokens that can be understood by the interpreter.

### Parser
The parser is exclusively responsible for syntax analysis and follows the predefined grammar (that was derived from the paper) for this purpose. After the syntax analysis the parser generates an "Abstract Snytax Tree" (AST).

### Interpreter
Now the interpreter can visit through the abstract syntax tree and validates for semantic correctness. Afterwards it returns the value.

## Execution
There are 2 files for executing verse code or the corresponding executables.
- First the [main.py](./modules/main.py) script file: this file allows the user to manipulate the variable `text` and change its string content to the desired verse code:
![main.py script](./pictures/main.py.png)

- Second, using the [Verse Console](./modules/verse_console.py): Here you can enter verse code like a command tool:
![console script](./pictures/console.png)

- Inside the Executable Directory you find 2 executables for either Windows and MacOS. Running them opens up a command console with the running script. The usability of the .EXE is the same as the Verse Console file.

## Test Cases
The File [Verse Interpreter Test](./modules/verse_interpreter_test.py) contains many test cases regarding the different features.

## Contributers
<p>
  <a href="https://github.com/Kariyampalli">
    <img src="https://img.shields.io/badge/Github-Christy-41BBC1"/>
  </a>
</p>
<p>
  <a href="https://github.com/Marcel-TO">
    <img src="https://img.shields.io/badge/Github-Marcel-3F3069"/>
  </a>
</p>

## License
This project is licensed under the MIT License. Feel free to use, modify, and distribute the code in accordance with the terms of the license.