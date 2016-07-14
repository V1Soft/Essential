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
                    masm += '\tidiv eax,' + operand2 + '\n'
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
   
