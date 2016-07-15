# Manual  

## Files
- **essl.py**: Main **File**
- **parser.py**: **Parser**
- **lexer.py**: **Lexer**
- **commands.py**: **Statements Handler**
- **utils.py**: Contains the needed **Utilities**
- **classes.py**: Contains the needed **Classes**

## Main File
This is the **file** that connects the **project** and calls the **parser**, **lexer**, and **compiler**. It is the top layer of the **program**.  

## Parser

## Lexer

## Statements Handler

## Utilities
There are two? **methods** contained in the **utilities file**.
- **getVar()** returns a corresponding **variable value**, if the **variable** doesn't exist, it returns a **string**  
  For example: 
  - ` %var ` will return ` 'var' `
  - ` NotAVar ` will return ` 'NotAVar' `

  **getVar()** also handles **mathematics** and **recursion**.  
  For **example**:
  - ` + 2 2 ` will return the corresponding **assembly code**.
  - ` function(functionAsArgument(argument)) ` will call the **recurse() function**.

- **recurse()** handles **recursion** and generates corresponding **assembly code**.
  For **example**: ` function(functionAsArgument(argument)) `  
  Since **return values** in Essential are stored in the ` eax ` **register**, **the output** is as follows:
  
  ```nasm
  push argument
  call functionAsArgument
  push eax
  call function
  ```
