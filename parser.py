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
            if inString:
                parsedScript[-1].append(classes.String(word))
            inString = not inString
        elif char == '\'' and not prevChar == '\\':
            inQuote = not inQuote
        elif char in ('+', '-', '*', '/'):
            if word:
                parsedScript[-1].append(word)
                word = ''
            parsedScript[-1].append(char)
        else:
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
