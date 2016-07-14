# Not entirely sure these are sane...

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
