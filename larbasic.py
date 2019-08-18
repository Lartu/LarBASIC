# +-----------------------+
# | LarBASIC™ Interpreter |
# |   by Martín del Río   |
# +-----------------------+

VERSION = 1
reserved = ["LET", "PRINT", "INPUT", "IF", "GOTO",
            "SLEEP", "END", "LIST", "REM", "READ",
            "WRITE", "APPEND", "RUN", "CLS", "CLEAR",
            "EXIT"]
operators = [["==", "!=", ">", "<", ">=", "<="],
             ["."],
             ["+", "-"],
             ["*", "/", "&", "|", "%"],
             ["^"]]
lines = {}
maxLine = 0
linePointer = 0
stopExecution = False
identifiers = {}
printReady = True

def main():
    print(f"LarBASIC version {VERSION}\nby Martín del Río (www.lartu.net)")
    while True:
            try:
                if printReady:
                    print("Ready.")
                nextLine = input()
                if len(nextLine) > 0:
                    executeTokens(lex(nextLine))
            except KeyboardInterrupt:
                pass
            except SystemExit:
                print("Bye!")
                break
            except:
                print("Execution halted.")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def getVarType(token):
    if len(token) > 1:
        if token[-1] == "$":
            return "STRING"
    return "NUM"

def isValidIdentifier(token):
    if len(token) == 0:
        return False
    if len(token) > 1:
        if token[-1] == "$":
            token = token[0:-1]
    if not(token[0].lower() in "abcdefghijklmnopqrstuvwxyz"):
        return False
    for c in token[1:]:
        if not(token[0].lower() in "abcdefghijklmnopqrstuvwxyz0123456789"):
            return False
    return True
    
def lex(line):
    # Splitteo la linea en varios tokens
    inString = False
    tokens = []
    currentToken = ""
    line = line + " "
    for c in line:
        if not(inString) and c in " ()\"":
            if len(currentToken) != 0:
                tokens.append([currentToken, "TBD"])
                currentToken = ""
            if c == '"':
                inString = True
        elif inString and c == '"':
            tokens.append([currentToken, "STRING"])
            currentToken = ""
            inString = False
        else:
            currentToken += c
    # Le asigno un tipo a cada token
    for token in tokens:
        if token[1] != "TBD":
            continue
        value = token[0]
        if is_number(value):
            token[0] = float(token[0])
            token[1] = "NUM" #Number
        elif value.upper() in reserved:
            token[0] = value.upper()
            token[1] = "RESVD" #Reserved word
        elif value.upper() == "THEN":
            token[0] = value.upper()
            token[1] = "THEN"
        elif value == "=":
            token[1] = "ASGN"
        elif isValidIdentifier(token[0]):
            token[1] = "ID" #Identifier
        else:
            for i in range(0, len(operators)):
                if token[0] in operators[i]:
                    token[1] = "OP"
    return tokens

def executeTokens(tokens):
    global lines, maxLine, stopExecution, linePointer, printReady
    printReady = True
    if tokens[0][1] == "NUM":
        lineNumber = int(tokens.pop(0)[0])
        if len(tokens) != 0:
            lines[lineNumber] = tokens
            if lineNumber > maxLine:
                maxLine = lineNumber
        else:
            lines.pop(lineNumber, None)
        printReady = False
        return
    if tokens[0][1] != "RESVD":
        print(f"Error: Unknown command {tokens[0][0]}.")
    else:
        command = tokens[0][0]
        if command == "REM":
            return
        elif command == "CLS":
            print("\n"*500)
        elif command == "END":
            stopExecution = True
        elif command == "EXIT":
            quit()
        elif command == "CLEAR":
            maxLine = 0
            lines = {}
            identifiers = {}
        elif command == "LIST":
            i = 0
            while i <= maxLine:
                if i in lines:
                    line = str(i)
                    for token in lines[i]:
                        tokenVal = ""
                        if token[1] == "NUM":
                            tokenVal = getNumberPrintFormat(token[0])
                        elif token[1] == "STRING":
                            tokenVal = f"\"{token[0]}\""
                        else:
                            tokenVal = token[0]
                        line += " " + str(tokenVal)
                    print(line)
                i = i + 1
        elif command == "PRINT":
            if not(printHandler(tokens[1:])): stopExecution = True
        elif command == "LET":
            if not(letHandler(tokens[1:])): stopExecution = True
        elif command == "INPUT":
            if not(inputHandler(tokens[1:])): stopExecution = True
        elif command == "GOTO":
            if not(gotoHandler(tokens[1:])): stopExecution = True
        elif command == "IF":
            if not(ifHandler(tokens[1:])): stopExecution = True
        elif command == "RUN":
            linePointer = 0
            while linePointer <= maxLine:
                if linePointer in lines:
                    executeTokens(lines[linePointer])
                    if stopExecution:
                        stopExecution = False
                        return
                linePointer = linePointer + 1

def getNumberPrintFormat(num):
    if int(num) == float(num):
        return int(num)
    return num

def gotoHandler(tokens):
    global linePointer
    if len(tokens) == 0:
        print("Error: Expected expression.")
        return
    newNumber = solveExpression(tokens, 0)
    if newNumber[1] != "NUM":
        print("Error: Line number expected.")
    else:
        linePointer = newNumber[0] - 1
    return True

def inputHandler(tokens):
    varName = None
    if len(tokens) == 0:
        print("Error: Expected identifier.")
        return
    elif len(tokens) == 1 and tokens[0][1] == "ID":
        varName = tokens[0][0]
    else:
        varName = solveExpression(tokens, 0)[0]
        if not(isValidIdentifier(varName)):
            print(f"Error: {varName} is not a valid identifier.")
            return
    while True:
        print("?", end = '')
        varValue = input()
        if getVarType(varName) == "STRING":
            identifiers[varName] = [varValue, "STRING"]
            break
        else:
            if is_number(varValue):
                identifiers[varName] = [varValue, "NUM"]
                break
            else:
                print("Try again.")
    return True

def ifHandler(tokens):
    thenPos = None
    for i in range(0, len(tokens)):
        if tokens[i][1] == "THEN":
            thenPos = i
            break
    if thenPos == None:
        print("Error: Malformed IF statement.")
        return
    exprValue = solveExpression(tokens[0:thenPos], 0)
    if exprValue == None:
        return
    elif exprValue[0] != 0:
        if len(tokens[i+1:]) == 0:
            print("Error: Malformed IF statement.")
            return      
        executeTokens(tokens[i+1:])
    return True

def letHandler(tokens):
    varName = None
    varValue = None
    eqPos = None
    for i in range(0, len(tokens)):
        if tokens[i][1] == "ASGN":
            eqPos = i
            break
    if eqPos == None:
        print("Error: Malformed LET statement.")
        return
    if eqPos == 1 and tokens[0][1] == "ID":
        varName = tokens[0][0]
    else:
        if len(tokens[0:i]) == 0:
            print("Error: Expected identifier.")
            return
        varName = solveExpression(tokens[0:i], 0)
        if varName == None:
            stopExecution = True
            return
        varName = varName[0]
        if not(isValidIdentifier(varName)):
            print(f"Error: {varName} is not a valid identifier.")
            return
    if len(tokens[i+1:]) == 0:
        print("Error: Expected expression.")
        return
    varValue = solveExpression(tokens[i+1:], 0)
    if varValue == None:
        return
    if getVarType(varName) != varValue[1]:
        print(f"Error: Variable {varName} type mismatch.")
        return
    identifiers[varName] = varValue
    return True

def printHandler(tokens):
    if len(tokens) == 0:
        print("Error: Expected identifier.")
        return
    exprRes = solveExpression(tokens, 0)
    if exprRes == None:
        return
    if exprRes[1] == "NUM":
        exprRes[0] = getNumberPrintFormat(exprRes[0])
    print(exprRes[0])
    return True

def getIdentifierValue(name):
    return identifiers[name]

def solveExpression(tokens, level):
    leftSideValues = []
    rightSideValues = []
    if level < len(operators):
        for i in range(0, len(tokens)):
            if not(tokens[i][1] in ["OP", "NUM", "STRING", "ID"]):
                print(f"Error: Unknown operand {tokens[i][0]}")
                return None
            elif tokens[i][1] == "OP" and tokens[i][0] in operators[level]:
                exprResL = None
                exprResR = None
                if len(leftSideValues) != 0:
                    exprResL = solveExpression(leftSideValues, level)
                rightSideValues = tokens[i+1:]
                if len(rightSideValues) != 0:
                    exprResR = solveExpression(rightSideValues, level)
                if exprResL == None or exprResR == None:
                    return None
                if tokens[i][0] == "+":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) + float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == "-":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) - float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == "/":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) / float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None 
                elif tokens[i][0] == "*":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) * float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None     
                elif tokens[i][0] == "^":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) ** float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == "%":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [float(exprResL[0]) % float(exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == "==":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] == exprResR[0], "NUM"]
                elif tokens[i][0] == "!=":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] != exprResR[0], "NUM"]
                elif tokens[i][0] == "<=":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] <= exprResR[0], "NUM"]
                elif tokens[i][0] == "<":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] < exprResR[0], "NUM"]
                elif tokens[i][0] == ">":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] > exprResR[0], "NUM"]
                elif tokens[i][0] == ">=":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        return [exprResL[0] >= exprResR[0], "NUM"]
                elif tokens[i][0] == "&":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [(exprResL[0]) and (exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == "|":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    elif exprResL[1] == "NUM" and exprResR[1] == "NUM":
                        return [(exprResL[0]) or (exprResR[0]), "NUM"]
                    else:
                        print("Error: Operand type mismatch.")
                        return None
                elif tokens[i][0] == ".":
                    if exprResL == None or exprResR == None:
                        print("Error: Operator expects value.")
                        return None
                    else:
                        value1 = exprResL[0]
                        if exprResL[1] == "NUM":
                            value1 = str(getNumberPrintFormat(value1))
                        value2 = exprResR[0]
                        if exprResR[1] == "NUM":
                            value2 = str(getNumberPrintFormat(value2))
                        return [value1 + value2, "STRING"]
                
            else:
                leftSideValues.append(tokens[i])
        return solveExpression(leftSideValues, level + 1)
    else:
        if len(tokens) > 1:
            print("Error: Operator expected.")
            return None
        elif tokens[0][1] == "ID":
            if tokens[0][0] in identifiers:
                return getIdentifierValue(tokens[0][0])
            else:
                print(f"Error: Variable {tokens[0][0]} not initialized.")
                return None
        return tokens[0]

main()