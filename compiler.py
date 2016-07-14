import utils
import commands

# Compile the script into assembly
def turingCompile(function):
    compiledScript = ''
    ifs = 0
    whiles = 0
    for word in function.value:
        if len(word) >= 1:
            if word[0][-2:] == '++':
                compiledScript += '\tmov ecx,' + getVar(word[0][:-2]) + '\n\tinc ecx\n\tmov [' + getVar(word[0][:-2]) + '],ecx\n\tint 80h\n'
            
            # Setting a variable
            elif word[1] == '=':

                if len(word) > 2:

                    # Define return value
                    if isinstance(word[2], list):
                        compiledScript += recurse(word[2])
                        
                        # Define an array segment
                        if isinstance(word[0], list):
                            if word[0][0] == 'list':
                                compiledScript += '\tmov ecx,' + word[0][1] + '\n\tadd ecx,' + str((int(word[0][2]) + 1)) + '\n\tmov [ecx],eax\n'
                                if not word[0][1] in variables:
                                    variables.append(word[0][1])
                        
                        # Define normal variable
                        else:
                            compiledScript += '\tmov [' + word[0] + '],eax\n'
                            if not word[0] in variables:
                                variables.append(word[0])
                else:
                    
                    # Define a list
                    if isinstance(word[2], list):
                        compiledScript += '\tmov ecx,' + word[0] + '\n'
                        for item in word[2]:
                            compiledScript += '\tadd ecx,1\n\tmov ebx,' + getVar(item) + '\n\tmov [ecx],ebx\n\tint 80h\n'
                        if not word[0] in variables:
                            variables.append(word[0])
                        
                    else:
                        
                        # Define an array segment
                        if isinstance(word[0], list):
                            if word[0][0] == 'list':
                                compiledScript += '\tmov ecx,' + word[0][1] + '\n\tadd ecx,' + str((int(word[0][2]) + 1)) + '\n\tmov ebx,' + getVar(word[2]) + '\n\tmov [ecx],ebx\n\tint 80h\n'
                                if not word[0][1] in variables:
                                    variables.append(word[0][1])
                        
                        # Define normal variable
                        else:
                            compiledScript += '\tmov ecx,' + getVar(word[2]) + '\n\tmov [' + word[0] + '],ecx\n\tint 80h\n'
                            if not word[0] in variables:
                                variables.append(word[0])
            
            # Contitional
            elif word[0] == 'if':
                whiles += 1
                turingCompile(classes.Variable(whilef, word[1:]))
            functions.append(classes.Variable(whilef, word[1:]))
            
            # Return a value
            elif word[0] == 'return':
                if function.key == 'main':
                    compiledScript += '\tmov eax,1\n\tmov ebx,[' + getVar(word[1]) + ']\n\tint 80h\n'
                else:
                    if isinstance(getVar(word[1]), list):
                        if getVar(word[1])[0] == 'math':
                            compiledScript += getVar(word[1])[1]
                    else:
                        compiledScript += '\tmov eax,' + str(getVar(word[1])) + '\n'

            # Inline Assembly
            elif word[0] == 'asm':
                compiledScript += word[1] + '\n'

        # Call a function
            else:
            
                # Call the main function
                if word[0] == 'main':
                    compiledScript += '\tcall _start\n'
                
                # Call other function
                else:
                    for item in word[1:]:
                        compiledScript += '\tpush ' + item + '\n'
                    compiledScript += '\tcall ' + word[0] + '\n'
    
    # Default exit '0'
    if function.key == 'main':
        compiledScript += '\tmov eax,1\n\tmov ebx,0\n\tint 80h\n'
    
    # Loop 'while' functions
    if function.key[0] == 'L':
        compiledScript += '\tloop ' + function.key + '\n'
    
    # Return normal functions
    else:
        compiledScript += '\tret\n'
    return compiledScript
