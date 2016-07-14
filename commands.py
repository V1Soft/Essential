# Not entirely sure these are sane...

def conditional(statement):
    compiledScript = ''
    for word in statement:
        
        # Compare an array
        if isinstance(word[0], classes.List):
            compiledScript += '\tmov ecx,' + utils.getVar(word[0].value[0]) + '\n\tadd ecx,' + utils.getVar(word[0].value[1]) + '\n'
                
        # Compare a normal variable
        else:
            #var = getVar(word[0][1])
            compiledScript += '\tmov ecx,[' + utils.getVar(word[0]).key + ']\n'
                
        # With an array
        if isinstance(word[2], classes.List):
            compiledScript += '\tmov ecx,' + utils.getVar(word[2].value[0]) + '\n\tadd ecx,' + utils.getVar(word[2].value[1]) + '\n'
                
        # With a normal variable
        else:
            var2 = utils.getVar(word[2])
                
        # EQUAL
        if word[1] == '==':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tje ' + iff + '\n\tint 80h\n'
                    
        # NOT EQUAL
        elif word[1] == '!=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjne ' + iff + '\n\tint 80h\n'
                
        # GREATER THAN
        elif word[1] == '>':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjg ' + iff + '\n\tint 80h\n'
                
        # LESS THAN
        elif word[1] == '<':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjl ' + iff + '\n\tint 80h\n'
                
        # GREATER THAN OR EQUAL TO
        elif word[1] == '>=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjge ' + iff + '\n\tint 80h\n'
                
        # LESS THAN OR EQUAL TO
        elif word[1] == '<=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjle ' + iff + '\n\tint 80h\n'
    return compiledScript

def loop(statement): # TODO: Fix
    compiledScript = ''
    for word in statement:
    
        # Compare an array
        if isinstance(word[0], classes.List):
            compiledScript += '\tmov ecx,[' + utils.getVar(word[0].value[0]) + ']\n\tadd ecx,' + utils.getVar(word[0].value[1]) + '\n'
                
        # Compare a normal variable
        else:
            compiledScript += '\tmov ecx,[' + utils.getVar(word[1]) + ']\n'
                
        # With an array
        if isinstance(word[2], classes.List):
            compiledScript += '\tmov ecx,' + utils.getVar(word[2].value[0]) + '\n\tadd ecx,' + utils.getVar(word[2].value[1]) + '\n'
                
        # With a normal variable
        else:
            var2 = utils.getVar(word[2])

        # EQUAL
        if word[0][2] == '==':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tje ' + whilef + '\n\tint 80h\n'
                
        # NOT EQUAL
        elif word[0][2] == '!=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjne ' + whilef + '\n\tint 80h\n'
                
        # GREATER THAN
        elif word[0][2] == '>':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjg ' + whilef + '\n\tint 80h\n'
                
        # LESS THAN
        elif word[0][2] == '<':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjl ' + whilef + '\n\tint 80h\n'
                
        # GREATER THAN OR EQUAL
        elif word[0][2] == '>=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjge ' + whilef + '\n\tint 80h\n'
                
        # LESS THAN OR EQUAL
        elif word[0][2] == '<=':
            compiledScript += '\tcmp ecx,[' + var2 + ']\n\tjle ' + whilef + '\n\tint 80h\n'
    return compiledScript
