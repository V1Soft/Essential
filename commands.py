def conditional(statement):
    compiledScript = ''

    # Compare an array
    if isinstance(word[0][1], list):
        if word[0][1][0] == 'list':
            compiledScript += '\tmov ecx,' + getVar(word[0][1][0]) + '\n\tadd ecx,' + getVar(word[0][1][1]) + '\n'
                
    # Compare a normal variable
    else:
        #var = getVar(word[0][1])
        compiledScript += '\tmov ecx,[' + getVar(word[0][1]).key + ']\n'
                
    # With an array
    if isinstance(word[0][3], list):
        if word[0][3][0] == 'list':
            compiledScript += '\tmov ecx,' + getVar(word[0][3][0]) + '\n\tadd ecx,' + getVar(word[0][3][1]) + '\n'
                
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
    return compiledScript

def loop(statement):
    compiledScript = ''
    
    # Compare an array
    if isinstance(word[0][1], list):
        if word[0][1][0] == 'list':
            var = getVar(word[0][1][0])
            compiledScript += '\tmov ecx,[' + var + ']\n\tadd ecx,' + getVar(word[0][1][1]) + '\n'
                
    # Compare a normal variable
    else:
        var = getVar(word[0][1])
        compiledScript += '\tmov ecx,[' + var + ']\n'
                
    # With an array
    if isinstance(word[0][3], list):
        if word[0][3][0] == 'list':
            var = getVar(word[0][3][0])
            compiledScript += '\tmov ecx,' + var + '\n\tadd ecx,' + getVar(word[0][3][1]) + '\n'
                
    # With a normal variable
    else:
        var2 = getVar(word[0][3])

    # EQUAL
    if word[0][2] == '==':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tje ' + whilef + '\n\tint 80h\n'
                
    # NOT EQUAL
    elif word[0][2] == '!=':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tjne ' + whilef + '\n\tint 80h\n'
                
    # GREATER THAN
    elif word[0][2] == '>':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tjg ' + whilef + '\n\tint 80h\n'
                
    # LESS THAN
    elif word[0][2] == '<':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tjl ' + whilef + '\n\tint 80h\n'
                
    # GREATER THAN OR EQUAL
    elif word[0][2] == '>=':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tjge ' + whilef + '\n\tint 80h\n'
                
    # LESS THAN OR EQUAL
    elif word[0][2] == '<=':
        compiledScript += '\tmov ecx,[' + var + ']\n\tcmp ecx,[' + var2 + ']\n\tjle ' + whilef + '\n\tint 80h\n'
