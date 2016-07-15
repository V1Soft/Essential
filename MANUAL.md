# Manual  

## Files
- **essl.py**: Main **File**
- **parser.py**: **Parser**
- **lexer.py**: **Lexer**
- **commands.py**: **Statements Handler**
- **utils.py**: Contains the needed **Utilities**
- **classes.py**: Contains the needed **Classes**

## Main File
This is the **file** that connects the **project** and calls the **parser**, **lexer**, and **compiler**. It is the top **layer** of the **program**.  

## Parser
- **parse(1)**
The **parser converts** the **plain text source** into a **format** the **compiler** can read. It also **reparses** the already parsed **script** and searches for ` end ` **tags**. Currently, it does not **error check punctuation** and **syntax**, nor **handle comments**; however, this is planned in future **development**.

## Lexer
- **lex(1)**
The **lexer** cycles through the **script** in search of ` if `, ` while `, and ` subroutine ` **tags**, and **appends** them to the **variable list**.

## Statements Handler
The **statements** handle Essential's **commands** and is used to **output** corresponding **code**. There are 3-4 **methods** in the **Commands File**.
- **conditional(1)** handles ` if ` **statements**.
- **loop(1)** handles ` while ` **statements**.
- **returnvalue(2)** handles **return values**.
- **asm(1)** handles **inline assembly**.

## Utilities
There are two **methods** contained in the **utilities file**.
- **getVar(1)** returns a corresponding **variable value**, if the **variable** doesn't exist, it returns a **string**  
  For example: 
  - ` %var ` will return ` 'var' `
  - ` NotAVar ` will return ` 'NotAVar' `

  **getVar(1)** also handles **mathematics** and **recursion**.  
  For **example**:
  - ` + 2 2 ` will return the corresponding **assembly code**.
  - ` function(functionAsArgument(argument)) ` will call the **recurse() function**.

- **recurse(1)** handles **recursion** and generates corresponding **assembly code**.
  For **example**: ` function(functionAsArgument(argument)) `  
  Since **return values** in Essential are stored in the ` eax ` **register**, **the output** is as follows:
  
  ```nasm
  push argument
  call functionAsArgument
  push eax
  call function
  ```
## Classes
- **Variable(2)** is the **variable object**. It is used to maintain generic **variables** for the **compiler**.
- **Args(1)** is the **argument object**. It is used to maintain **functions' arguments** for **recurse(1)**.
- **String(1)** is the **string object**. It is used to identify **strings**.
- **List(1)** is the **list object**. It is used to identify **lists**.
