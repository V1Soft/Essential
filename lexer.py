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

import classes
import parser

# Defining all variables
def lex(parsedScript):
    lexedScript = parsedScript
    functions = []
    index = 0
    for structure in parsedScript:
        if structure[0] == 'use':
            proto = ''
            pkg = ''
            if structure[1].startswith('.'):
                proto = structure[1][1:]
            else:
                proto = '/' + structure[1]
            for char in proto:
                if char == '.':
                    pkg += '/'
                elif char == '/':
                    print('Error: Invalid Syntax.')
                    sys.exit(1)
                else:
                    pkg += char
            lex(parser.parse(open(pkg + '.essl', 'r+').read()))
        elif structure[0][0] == 'subroutine':
            functions.append(classes.Variable(structure[0][1], structure[1:]))
            lexedScript[index].remove(structure[0])
        index += 1
    return functions
