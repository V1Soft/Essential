#########################################################################
# Copyright (C) 2016 ecoh70                                             #
#                                                                       #
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or (at #
# your option) any later version.                                       #
#                                                                       #
# This program is distributed in the hope that it will be useful, but   #
# WITHOUT ANY WARRANTY; without even the implied warranty of            #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU     #
# General Public License for more details.                              #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

import sys
import os

functions = []
variables = []
ifequFunc = '%macro ifequ 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tje %3\n\tint 80h\n%endmacro\n\n'
ifequsFunc = '%macro ifequs 4\n\tmov esi,%1\n\tmov edi,%2\n\tmov ecx,%3\n\tcld\n\trepe cmpsb\n\tjecxz %4\n\tint 80h\n%endmacro\n\n'
ifneFunc = '%macro ifne 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tjne %3\n\tint 80h\n%endmacro\n\n'
ifnesFunc = '%macro ifnes 4\n\tmov esi,%1\n\tmov edi,%2\n\tmov ecx,%3\n\tcld\n\trepe cmpsb\n\tjne %4\n\tint 80h\n%endmacro\n\n'
ifgtFunc = '%macro ifgt 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tjg %3\n\tint 80h\n%endmacro\n\n'
ifltFunc = '%macro iflt 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tjl %3\n\tint 80h\n%endmacro\n\n'
ifgeFunc = '%macro ifge 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tjge %3\n\tint 80h\n%endmacro\n\n'
ifleFunc = '%macro ifle 3\n\tmov ecx,[%1]\n\tcmp ecx,[%2]\n\tjle %3\n\tint 80h\n%endmacro\n\n'
ifFuncs = [ifequFunc, ifequsFunc, ifneFunc, ifnesFunc, ifgtFunc, ifltFunc, ifgeFunc, ifleFunc]
printFunc = '%macro print 2\n\tmov edx,%2\n\tmov ecx,%1\n\tmov ebx,1\n\tmov eax,4\n\tint 80h\n%endmacro\n\n'
readFunc = '%macro read 1\n\tmov eax,3\n\tmov ebx,2\n\tmov ecx,%1\n\tmov edx,5\n\tint 80h\n%endmacro\n\n'
exitFunc = '%macro exit 1\n\tmov eax,1\n\tmov ebx,%1\n\tint 80h\n%endmacro\n\n'

# Define Variable Object
class Variable(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

# Get Variable. If non-existant, return string
def getVar(key):
    if key[0] == '%':
        if key[1:] in variables:
            for var in variables:
                if var.key == key[1:]:
                    return var
    else:
        return Variable(key, str(key))

# Parse the Essential Script
def parse(source):
    parsedScript = [[]]
    word = ''
    inNode = False
    inString = False
    inQuote = False
    for char in source:
        if char in (';', '\n') and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
            parsedScript.append([])
        elif char == '(':
            parsedScript.append([])
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char == ')' and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
            temp = parsedScript.pop()
            parsedScript[-1].append(temp)
        elif char in (' ', '\t') and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char == '\"':
            inString = not inString
        elif char == '\'':
            inQuote = not inQuote
        else:
            word += char
    if word:
        parsedScript[-1].append(word)
        word = ''
    reparsedScript = [[]]
    
    # Parse multi-line code until 'end'
    for word in parsedScript:
        if word:
            if word[0] in ('function', 'if', 'for', 'while'):
                reparsedScript.append([])
                reparsedScript[-1].append(word)
            elif word[0] == 'end':
                temp = reparsedScript.pop()
                reparsedScript[-1].append(temp)
            else:
                reparsedScript[-1].append(word)
    return reparsedScript[0]

# Defining all variables
def lex(parsedScript):
    lexedScript = parsedScript
    print(lexedScript)
    index = 0
    for structure in parsedScript:
        if structure[0][0] == 'function':
            functions.append(Variable(structure[0][1], structure[1:]))
            lexedScript[index].remove(structure[0])
        index += 1

# Compile the script into assembly
def turingCompile(function):
    compiledScript = ''
    ifs = 0
    whiles = 0
    for word in function.value:
        if len(word) > 1:
            
            # Setting a variable
            if word[1] == '=':
                
                # Math Operations
                if len(word) > 3:
                    
                    # Add
                    if word[3] == '+':
                        var = getVar(word[2])
                        var2 = getVar(word[4])
                        
                        # Define an array segment
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str(int(word[0][1]) + 1) + '\n\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tadd eax,ebx\n\tmov [ecx],eax\n\tint 80h\n'
                        
                        # Define a normal variable
                        else:
                            compiledScript += '\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tadd eax,ebx\n\tmov [' + word[0] + '],eax\n\tint 80h\n'
                    
                    # Subtract
                    elif word[3] == '-':
                        var = getVar(word[2])
                        var2 = getVar(word[4])
                        
                        # Define an array segment
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str(int(word[0][1]) + 1) + '\n\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tsub eax,ebx\n\tmov [ecx],eax\n\tint 80h\n'
                        
                        # Define a normal variable
                        else:
                            compiledScript += '\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tsub eax,ebx\n\tmov [' + word[0] + '],eax\n\tint 80h\n'
                else:
                    
                    # Define a list
                    if isinstance(word[2], list):
                        compiledScript += '\tmov ecx,' + word[0] + '\n'
                        for item in word[2]:
                            compiledScript += '\tadd ecx,1\n\tmov ebx,' + item + '\n\tmov [ecx],ebx\n\tint 80h\n'
                        variables.append(Variable(word[0], word[2]))
                    else:
                        
                        # Define an array segment
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str((int(word[0][1]) + 1)) + '\n\tmov ebx,' + word[2] + '\n\tmov [ecx],ebx\n\tint 80h\n'
                        
                        # Define normal variable
                        else:
                            compiledScript += '\tmov ecx,' + word[2] + '\n\tmov [' + word[0] + '],ecx\n\tint 80h\n'
                            variables.append(Variable(word[0], word[2]))
            
            # Conditional
            elif word[0][0] == 'if':
                
                # Compare an array
                if isinstance(word[0][1], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][1][0]) + '\n\tadd ecx,' + word[0][1][1] + '\n'
                
                # Compare a normal variable
                else:
                    var = getVar(word[0][1])
                    compiledScript += '\tmov ecx,[' + var.key + ']\n'
                
                # With an array
                if isinstance(word[0][3], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][3][0]) + '\n\tadd ecx,' + word[0][3][1] + '\n'
                
                # With a normal variable
                else:
                    var2 = getVar(word[0][3])
                    
                # Define the 'if' function
                iff = '.if' + str(hex(ifs)[2:])
                functions.append(Variable(iff, word[1:]))
                
                # EQUAL
                if word[0][2] == '==':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tje ' + iff + '\n\tint 80h\n'
                    
                # NOT EQUAL
                elif word[0][2] == '!=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjne ' + iff + '\n\tint 80h\n'
                
                # GREATER THAN
                elif word[0][2] == '>':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjg ' + iff + '\n\tint 80h\n'
                
                # LESS THAN
                elif word[0][2] == '<':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjl ' + iff + '\n\tint 80h\n'
                
                # GREATER THAN OR EQUAL TO
                elif word[0][2] == '>=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjge ' + iff + '\n\tint 80h\n'
                
                # LESS THAN OR EQUAL TO
                elif word[0][2] == '<=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjle ' + iff + '\n\tint 80h\n'
                ifs += 1
                
            # Loop
            elif word[0][0] == 'while':
                
                # Compare an array
                if isinstance(word[0][1], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][1][0]) + '\n\tadd ecx,' + word[0][1][1] + '\n'
                
                # Compare a normal variable
                else:
                    var = getVar(word[0][1])
                    compiledScript += '\tmov ecx,[' + var.key + ']\n'
                
                # With an array
                if isinstance(word[0][3], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][3][0]) + '\n\tadd ecx,' + word[0][3][1] + '\n'
                
                # With a normal variable
                else:
                    var2 = getVar(word[0][3])
                    
                # Define 'while' function
                whilef = '.L' + str(hex(whiles)[2:])
                
                # EQUAL
                if word[0][2] == '==':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tje ' + iff + '\n\tint 80h\n'
                
                # NOT EQUAL
                elif word[0][2] == '!=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjne ' + iff + '\n\tint 80h\n'
                
                # GREATER THAN
                elif word[0][2] == '>':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjg ' + iff + '\n\tint 80h\n'
                
                # LESS THAN
                elif word[0][2] == '<':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjl ' + iff + '\n\tint 80h\n'
                
                # GREATER THAN OR EQUAL
                elif word[0][2] == '>=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjge ' + iff + '\n\tint 80h\n'
                
                # LESS THAN OR EQUAL
                elif word[0][2] == '<=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjle ' + iff + '\n\tint 80h\n'
                whiles += 1
                turingCompile(Variable('function', whilef, word[1:]))
            
            # Return a value
            elif word[0] == 'return':
                compiledScript += '\tmov eax,' + word[1] + '\n'
            
            # System exit
            elif word[0] == 'exit':
                
                # Exit with array segment
                if isinstance(word[1], list):
                    compiledScript += '\tmov ecx,' + word[1][0][1:] + '\n\tadd ecx,' + str(int(word[1][1]) + 1) + '\n\tmov eax,1\n\tmov ebx,[ecx]\n\tint 80h\n'
                
                # Exit with normal variable
                else:
                    compiledScript += '\tmov eax,1\n\tmov ebx,[' + getVar(word[1]).key + ']\n\tint 80h\n'
            
            # Inline Assembly
            elif word[0] == 'asm':
                compiledScript += word[1] + '\n'
        
        # Call a function
        else:
            
            # Call the main function
            if word[0][0] == 'main':
                compiledScript += '\tcall _start\n'
                
            # Call other function
            else:
                compiledScript += '\tcall .' + word[0][0] + '\n'
    
    # Default exit '0'
    if function.key == 'main':
        compiledScript += '\tmov eax,1\n\tmov ebx,0\n\tint 80h\n'
    
    # Loop 'while' functions
    elif function.key[0] == 'L':
        compiledScript += '\tloop ' + function.key + '\n'
    
    # Return normal functions
    else:
        compiledScript += '\tint 80h\n\tret\n'
    return compiledScript
asm = ''

# Parse and lex the file
lex(parse(open(sys.argv[1], 'r+').read()))

# Compile all functions
for function in functions:
    
    # Define main function as '_start'
    if function.key == 'main':
        asm += 'section .text\n\tglobal _start\n\n' + '_start:\n'
    
    # Define normal function
    else:
        asm += function.key + ':\n'
    asm += turingCompile(function)
    
# Compile all variables
asm += '\nsection .data\n'
for var in variables:
    asm += '\tglobal ' + var.key + '\n' + var.key + ':\n'
    
    # Define array segment
    if isinstance(var.value, list):
        for item in var.value:
            asm += '\tdb ' + item + '\n'
    
    # Define normal variable
    else:
        asm += '\tdb ' + item + '\n'

# Show final compilation
print(asm)

# Compile
os.system('echo "' + asm + '" > ' + sys.argv[1].split('.')[0] + '.asm')

# Assemble
os.system('nasm -f elf ' + sys.argv[1].split('.')[0] + '.asm')

# Link
os.system('ld -m elf_i386 -s -o ' + sys.argv[1].split('.')[0] + ' ' + sys.argv[1].split('.')[0] + '.o')
