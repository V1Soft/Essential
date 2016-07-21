#! /usr/bin/python3

# Copyright (c) 2016, Connor E. Haight <connor.haight@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the VectorOne nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
