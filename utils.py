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

# Get Variable. If non-existant, return string
def getVar(key):
    if key[0] == '%':
        try:
            return '[esp + ' + str(int(key[1:])*4) + ']'
        except ValueError:
            return key[1:]
    elif key[0] == 'args' and key[1] in ('+', '-', '/', '*'):
        msrc = key[1:]
        i = len(msrc) - 1
        mexp = []
        masm = ''
        while i > -1:
            if not msrc[i] in ('+', '-', '*', '/'):
                masm += recurse(msrc[i])
                mexp.append(getVar(msrc[i]))
            elif msrc[i] in ('+', '-', '/', '*'):
                operand = mexp.pop()
                operand2 = mexp.pop()
                if msrc[i] == '+':
                    masm += '\tadd eax,' + operand2 + '\n'
                elif msrc[i] == '-':
                    masm += '\tsub eax,' + operand2 + '\n'
                elif msrc[i] == '*':
                    masm += '\timul eax,' + operand2 + '\n'
                elif msrc[i] == '/':
                    masm += '\tidiv eax,' + operand2 + '\n' # doesn't work
                mexp.append('eax')
            i -= 1
        return ['math', masm]
    else:
        if key == 'null':
            return '0x00'
        elif key == 'true':
            return '1'
        elif key == 'false':
            return '0'
        else:
            return key

# Handle Recursion
def recurse(source):
    compiledScript = ''
    if source[0] == 'args' and not source[1] in ('+', '-', '*', '/'):
        for arg in source[2:]:
            if isinstance(arg, list):
                compiledScript += recurse(arg) + '\tpush eax\n'
            else:
                compiledScript += '\tpush ' + getVar(arg) + '\n'
        compiledScript += '\tcall ' + source[1] + '\n'
    else:
        if isinstance(getVar(source), list):
            if getVar(source)[0] == 'math':
                compiledScript += getVar(source)[1]
        #else:
        #    compiledScript += getVar(source)# + '\n'
    return compiledScript
   
