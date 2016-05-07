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

class Variable(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

def getVar(key):
    if key[0] == '%':
        if key[1:] in variables:
            for var in variables:
                if var.key == key[1:]:
                    return var
    else:
        return Variable(key, str(key))

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

def lex(parsedScript):
    lexedScript = parsedScript
    print(lexedScript)
    index = 0
    for structure in parsedScript:
        if structure[0][0] == 'function':
            functions.append(Variable(structure[0][1], structure[1:]))
            lexedScript[index].remove(structure[0])
        index += 1

def turingCompile(function):
    compiledScript = ''
    ifs = 0
    whiles = 0
    for word in function.value:
        if len(word) > 1:
            if word[1] == '=':
                if len(word) > 3:
                    if word[3] == '+':
                        var = getVar(word[2])
                        var2 = getVar(word[4])
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str(int(word[0][1]) + 1) + '\n\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tadd eax,ebx\n\tmov [ecx],eax\n\tint 80h\n'
                        else:
                            compiledScript += '\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tadd eax,ebx\n\tmov [' + word[0] + '],eax\n\tint 80h\n'
                    elif word[3] == '-':
                        var = getVar(word[2])
                        var2 = getVar(word[4])
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str(int(word[0][1]) + 1) + '\n\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tsub eax,ebx\n\tmov [ecx],eax\n\tint 80h\n'
                        else:
                            compiledScript += '\tmov eax,' + var.key + '\n\tmov ebx,' + var2.key + '\n\tsub eax,ebx\n\tmov [' + word[0] + '],eax\n\tint 80h\n'
                else:
                    if isinstance(word[2], list):
                        compiledScript += '\tmov ecx,' + word[0] + '\n'
                        for item in word[2]:
                            compiledScript += '\tadd ecx,1\n\tmov ebx,' + item + '\n\tmov [ecx],ebx\n\tint 80h\n'
                        variables.append(Variable(word[0], word[2]))
                    else:
                        if isinstance(word[0], list):
                            compiledScript += '\tmov ecx,' + word[0][0] + '\n\tadd ecx,' + str((int(word[0][1]) + 1)) + '\n\tmov ebx,' + word[2] + '\n\tmov [ecx],ebx\n\tint 80h\n'
                        else:
                            compiledScript += '\tmov ecx,' + word[2] + '\n\tmov [' + word[0] + '],ecx\n\tint 80h\n'
                            variables.append(Variable(word[0], word[2]))
            elif word[0][0] == 'if':
                if isinstance(word[0][1], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][1][0]) + '\n\tadd ecx,' + word[0][1][1] + '\n'
                else:
                    var = getVar(word[0][1])
                    compiledScript += '\tmov ecx,[' + var.key + ']\n'
                if isinstance(word[0][3], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][3][0]) + '\n\tadd ecx,' + word[0][3][1] + '\n'
                else:
                    var2 = getVar(word[0][3])
                iff = '.if' + str(hex(ifs)[2:])
                functions.append(Variable(iff, word[1:]))
                if word[0][2] == '==':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tje ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '!=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjne ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '>':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjg ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '<':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjl ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '>=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjge ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '<=':
                    compiledScript += '\tcmp ecx,[' + var2.key + ']\n\tjle ' + iff + '\n\tint 80h\n'
                ifs += 1
            elif word[0][0] == 'while':
                if isinstance(word[0][1], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][1][0]) + '\n\tadd ecx,' + word[0][1][1] + '\n'
                else:
                    var = getVar(word[0][1])
                    compiledScript += '\tmov ecx,[' + var.key + ']\n'
                if isinstance(word[0][3], list):
                    compiledScript += '\tmov ecx,' + getVar(word[0][3][0]) + '\n\tadd ecx,' + word[0][3][1] + '\n'
                else:
                    var2 = getVar(word[0][3])
                whilef = '.L' + str(hex(whiles)[2:])
                if word[0][2] == '==':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tje ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '!=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjne ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '>':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjg ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '<':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjl ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '>=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjge ' + iff + '\n\tint 80h\n'
                elif word[0][2] == '<=':
                    compiledScript += '\tmov ecx,[' + var.key + ']\n\tcmp ecx,[' + var2.key + ']\n\tjle ' + iff + '\n\tint 80h\n'
                whiles += 1
                turingCompile(Variable('function', whilef, word[1:]))
            elif word[0] == 'return':
                compiledScript += '\tmov eax,' + word[1] + '\n'
            elif word[0] == 'exit':
                if isinstance(word[1], list):
                    compiledScript += '\tmov ecx,' + word[1][0][1:] + '\n\tadd ecx,' + str(int(word[1][1]) + 1) + '\n\tmov eax,1\n\tmov ebx,[ecx]\n\tint 80h\n'
                else:
                    compiledScript += '\tmov eax,1\n\tmov ebx,[' + getVar(word[1]).key + ']\n\tint 80h\n'
            elif word[0] == 'asm':
                compiledScript += word[1] + '\n'
        else:
            if word[0][0] == 'main':
                compiledScript += '\tcall _start\n'
            else:
                compiledScript += '\tcall .' + word[0][0] + '\n'
    if function.key == 'main':
        compiledScript += '\tmov eax,1\n\tmov ebx,0\n\tint 80h\n'
    elif function.key[0] == 'L':
        compiledScript += '\tloop ' + function.key + '\n'
    else:
        compiledScript += '\tint 80h\n\tret\n'
    return compiledScript
asm = ''
lex(parse(open(sys.argv[1], 'r+').read()))
for function in functions:
    if function.key == 'main':
        #for ifFunc in ifFuncs:
            #asm += ifFunc
        asm += 'section .text\n\tglobal _start\n\n' + '_start:\n'
    else:
        asm += function.key + ':\n'
    asm += turingCompile(function)
asm += '\nsection .data\n'
for var in variables:
    asm += '\tglobal ' + var.key + '\n' + var.key + ':\n'
    if isinstance(var.value, list):
        for item in var.value:
            asm += '\tdb ' + item + '\n'
    else:
        asm += '\tdb ' + item + '\n'

print(asm)

os.system('echo "' + asm + '" > ' + sys.argv[1].split('.')[0] + '.asm')
os.system('nasm -f elf ' + sys.argv[1].split('.')[0] + '.asm')
os.system('ld -m elf_i386 -s -o ' + sys.argv[1].split('.')[0] + ' ' + sys.argv[1].split('.')[0] + '.o')
