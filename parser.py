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

# Parse the Essential Script
def parse(source):
    parsedScript = [[]]
    word = ''
    prevChar = ''
    inArgs = False
    inList = False
    inString = False
    inQuote = False
    for char in source:
        if char == '(' and not inString and not inQuote:
            parsedScript.append([])
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char in (';', '\n') and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
            parsedScript.append([])
        elif char == '[':
            parsedScript.append([])
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char in ')' and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
            temp = parsedScript.pop()
            parsedScript[-1].append(temp)
            args_t = parsedScript[-1]
            parsedScript.remove(args)
            parsedScript[-1].append(classes.Args(args))
        elif char == ']' and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
            temp = parsedScript.pop()
            parsedScript[-1].append(temp)
            list_t = parsedScript[-1]
            parsedScript.remove(list_t)
            parsedScript[-1].append(classes.List(list_t))
        elif char in (' ', '\t') and not inString and not inQuote:
            if word:
                parsedScript[-1].append(word)
                word = ''
        elif char == '\"' and not prevChar == '\\':
            inString = not inString
        elif char == '\'' and not prevChar == '\\':
            inQuote = not inQuote
        elif char in ('=', '+', '-', '*', '/'):
            if word:
                parsedScript[-1].append(word)
                word = ''
            word += char
        else:
            if prevChar in ('=', '+', '-', '*', '/'):
                if word:
                    parsedScript[-1].append(word)
                    word = ''
            word += char
            prevChar = char
    if word:
        parsedScript[-1].append(word)
        word = ''
    reparsedScript = [[]]
    
    # Parse multi-line code until 'end'
    for word in parsedScript:
        if word:
            if word[0] in ('subroutine', 'if', 'for', 'while'):
                reparsedScript.append([])
                reparsedScript[-1].append(word)
            elif word[0] == 'end':
                temp = reparsedScript.pop()
                reparsedScript[-1].append(temp)
            else:
                reparsedScript[-1].append(word)
    return reparsedScript[0]
