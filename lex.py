# Defining all variables
def lex(parsedScript):
    lexedScript = parsedScript
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
            lex(parse(open(pkg + '.essl', 'r+').read()))
        elif structure[0][0] == 'subroutine':
            functions.append(Variable(structure[0][1], structure[1:]))
            lexedScript[index].remove(structure[0])
        index += 1
