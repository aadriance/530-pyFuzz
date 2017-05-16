import sys
from controlFlow import *
from fuzzUtil import *
import re
import subprocess

#Written in python 3

#global variables, bc quick software design
whiteSpace = ''
callQueue = []
prevLine = ''
funcList = []

#processLine takes in lines of the file one by one
#If the line is a def line, insert the print and add the function to the call Queue
#If we are out of the function (IE only a new line) pull the function off the callQueue andd add an exit statement
def processLine(line):
    global callQueue
    global prevLine
    
    origLine = line
    
    #incase you aren't just one indent in, find all the space
    space = getSpace(line)

    if(len(line.lstrip()) > 0 and len(space) == 0 and not isComment(line) and len(callQueue) > 0):
        outFunc = callQueue[len(callQueue)-1]
        line = whiteSpace + 'exitFunction()\n' + line
        callQueue = callQueue[0:len(callQueue)-1]

    #if main exists
    if isMain(origLine):
        mainspace = getSpace(origLine)
        #if __name__ == "__main__":
        if(len(mainspace) > 0):
            line = mainspace + 'try:\n'
            for f in funcList:
                line +=  mainspace + mainspace + 'registerFunc(\''+ f +'\')\n' 
            line += mainspace + origLine + '\n' + mainspace + 'except:\n' +\
               (mainspace*2) + 'print(\'Crash!\')\n'+(mainspace*2) +'prettyPrint()\n' + (mainspace*2) + 'exit(57)\n'
        else:
            #line comes from earlier if statement. replacing the value here to add try/except
            line = whiteSpace + 'exitFunction()\n'
            line += 'try:\n' + whiteSpace + origLine + '\n' + 'except:\n' + whiteSpace + 'print(\'Crash!\')\n'+whiteSpace +'prettyPrint()\n'

    elif isFunc(origLine):
        inFunc = origLine.replace('def ', '').replace(':\n','')
        #close function
        line += whiteSpace + 'makeControlFlow(\'' + inFunc.replace('\'', '\\\'') + '\')\n'
        callQueue.append(inFunc)
        funcList.append(inFunc)

    #close function, but leave on the queue since it's a return
    elif isReturn(line) and len(callQueue) > 0 :
        outFunc = callQueue[len(callQueue)-1]
        line = space + 'exitFunction()\n' + line
    prevLine = line
    return line

#Returns the count of leading whitespace
def whiteSpaceCount(line, hi):
    return len(line) - len(line.lstrip())

#check if line is comment
def isComment(line):
    return (line.lstrip())[0] == '#'

#check if line is a return
def isReturn(line):
    return (line.lstrip())[0:6] == 'return'

#check if line is a function def
def isFunc(line):
    return line[0:4] == 'def '

def isMain(line):
    return (line.lstrip())[0:6] == 'main()'

#Reads the file until it find a line with whitespace
#Records the whitespace so we can replicate it later
def findWhiteSpace(inFile):
    inData = open(inFile, 'r')
    global whiteSpace
    for line in inData:
        if len(line.lstrip()) != len(line) and len(line.lstrip()) != 0:
            whiteSpace = getSpace(line)

#copies the white space for that line
def getSpace(line):
    space = ''
    for c in line:
        if c.isspace():
            space += c
        else:
            return space
    return space

def makeArgs(parmList):
    args = []
    for arg in parmList:
        if arg == 'int':
            args.append(str(0))
        if arg == 'string':
            args.append('foo')
    return args

#Takes one command line argument for the file name
def main():
    if len(sys.argv) < 4:
        print('Please provide a file name and run count')
        print('pyFuzz inFile run# \'(parmList)\'')
        exit(1)
    inFile = sys.argv[1]
    runCount = int(sys.argv[2])
    parmList = sys.argv[3].split(', ')
    findWhiteSpace(inFile)
    inData = open(inFile, 'r')
    outData = open('tooled_' + inFile, 'w')
    #outData = open('tooled_' + inFile, 'a')
    #bring fuzz util into the tooled file
    outData.write('from fuzzUtil import *\n')
    for line in inData:
        outData.write(processLine(line))
    outData.close()
    inData.close()
    for i in range(0,runCount):
        exCode = subprocess.run(["python3", 'tooled_' + inFile] + makeArgs(parmList))
        print(exCode)

if __name__ == "__main__":
    main()

