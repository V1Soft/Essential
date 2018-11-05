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

# TODO: Create classes for type

# TODO: Create the following functions to use here and elsewhere:
#LoadArray()
#LoadVariable()

# TODO: Separate conditional() into separate methods
#ConditionalCompareEqual()
#ConditionalCompareNotEqual()
#ConditionalCompareGreater()
#ConditionalCompareLess()
#ConditionalCompareGreaterOrEqual()
#ConditionalCompareLesserOrEqual()

# TODO: Separate loop() into separate methods
#LoopCompareEqual()
#LoopCompareNotEqual()
#LoopCompareGreater()
#LoopCompareLess()
#LoopCompareGreaterOrEqual()
#LoopCompareLesserOrEqual()

def conditional(statement):
    compiledScript = ''
    
    # Compare an array
    if isinstance(statement[0], classes.List):
        compiledScript += '\tmov ecx,' + utils.getVar(statement[0].value[0]) + '\n\tadd ecx,' + utils.getVar(statement[0].value[1]) + '\n'
                
    # Compare a normal variable
    else:
        #var = getVar(word[0][1])
        compiledScript += '\tmov ecx,[' + utils.getVar(statement[0]).key + ']\n'
                
    # With an array
    if isinstance(statement[2], classes.List):
        compiledScript += '\tmov ecx,' + utils.getVar(statement[2].value[0]) + '\n\tadd ecx,' + utils.getVar(statement[2].value[1]) + '\n'
                
    # With a normal variable
    else:
        var2 = utils.getVar(statement[2])
                
    # EQUAL
    if statement[1] == '==':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tje ' + iff + '\n\tint 80h\n'
                    
    # NOT EQUAL
    elif statement[1] == '!=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjne ' + iff + '\n\tint 80h\n'
                
    # GREATER THAN
    elif statement[1] == '>':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjg ' + iff + '\n\tint 80h\n'
                
    # LESS THAN
    elif statement[1] == '<':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjl ' + iff + '\n\tint 80h\n'
                
    # GREATER THAN OR EQUAL TO
    elif statement[1] == '>=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjge ' + iff + '\n\tint 80h\n'
                
    # LESS THAN OR EQUAL TO
    elif statement[1] == '<=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjle ' + iff + '\n\tint 80h\n'
    return compiledScript

def loop(statement):
    compiledScript = ''

    # Compare an array
    if isinstance(word[0], classes.List):
        compiledScript += '\tmov ecx,[' + utils.getVar(statement[0].value[0]) + ']\n\tadd ecx,' + utils.getVar(word[0].value[1]) + '\n'
            
    # Compare a normal variable
    else:
        compiledScript += '\tmov ecx,[' + utils.getVar(statement[1]) + ']\n'
            
    # With an array
    if isinstance(statement[2], classes.List):
        compiledScript += '\tmov ecx,' + utils.getVar(statement[2].value[0]) + '\n\tadd ecx,' + utils.getVar(statement[2].value[1]) + '\n'
                
    # With a normal variable
    else:
        var2 = utils.getVar(statement[2])

    # EQUAL
    if statement[1] == '==':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tje ' + whilef + '\n\tint 80h\n'
                
    # NOT EQUAL
    elif statement[1] == '!=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjne ' + whilef + '\n\tint 80h\n'
                
    # GREATER THAN
    elif statement[1] == '>':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjg ' + whilef + '\n\tint 80h\n'
                
    # LESS THAN
    elif statement[1] == '<':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjl ' + whilef + '\n\tint 80h\n'
            
    # GREATER THAN OR EQUAL
    elif statement[1] == '>=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjge ' + whilef + '\n\tint 80h\n'
                
    # LESS THAN OR EQUAL
    elif statement[1] == '<=':
        compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjle ' + whilef + '\n\tint 80h\n'
    return compiledScript

def returnvalue(function, statement):
    compiledScript = ''

    if function.key == 'main':
        compiledScript += '\tmov eax,1\n\tmov ebx,[' + utils.getVar(statement[0]) + ']\n\tint 80h\n'
    else:
        if isinstance(getVar(statement[0]), list):
            if utils.getVar(statement[0])[0] == 'math':
                compiledScript += utils.getVar(statement[0])[1]
        else:
            compiledScript += '\tmov eax,' + str(utils.getVar(statement[0])) + '\n'
    return compiledScript
