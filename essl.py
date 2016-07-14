#! /usr/bin/python3

import sys
import os

import classes
import parser
import lexer
import compiler

functions = []
variables = []

asm = ''

# Parse and lex the file
lexer.lex(parser.parse(open(sys.argv[1], 'r+').read()))

# Compile all functions
for function in functions:
    
    # Define main function as '_start'
    if function.key == 'main':
        asm += 'section .text\n\tglobal _start\n\n' + '_start:\n'
    
    # Define normal function
    else:
        asm += function.key + ':\n'
    asm += compiler.turingCompile(function)
    
# Compile all variables
asm += '\nsection .bss\n'
for var in variables:
    asm += '\tglobal ' + var + '\n'
for var in variables:
    asm += var + ':\n'
    asm += '\tresb 1\n'

# Show final compilation
print(asm)

# Compile
os.system('echo "' + asm + '" > ' + sys.argv[1].split('.')[0] + '.asm')

# Assemble
os.system('nasm -f elf ' + sys.argv[1].split('.')[0] + '.asm')

# Link
os.system('ld -m elf_i386 -s -o ' + sys.argv[1].split('.')[0] + ' ' + sys.argv[1].split('.')[0] + '.o')
