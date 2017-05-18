import sys
from controlFlow import *
from fuzzUtil import *
import re
import subprocess
import random
import string
from shutil import copyfile
from os import rename

#Written in python 3

#global variables, bc quick software design
whiteSpace = ''
callQueue = []
prevLine = ''
funcList = []
flowList = []

INTMAX = 4000000

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
        funcList.append(re.split(r'[(, )]', inFunc)[0])

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
    #args is tuple of type and value
    args = []
    for arg in parmList:
        if arg == 'int':
            args.append(('int', str(0)))
        elif arg == 'string':
            args.append(('string', 'foo'))
        elif arg.startswith("file:"):
            #append "_fuzzed" to file name 
            src = arg.replace("file:", "")
            copyfile(src, src + "_fuzzed")
            args.append(('file', src + "_fuzzed"))
        elif arg.startswith("static:"):
            args.append(('static', arg.replace("static:", "")))
        else:
            print("Invalid argument")
            exit(1)
    return args

def fuzzInt():
    return random.randint(0, INTMAX)

def fuzzString():
    #choose length
    leng = random.randint(1, 100)
    st = ""
    for i in range(leng):
       st += random.choice(string.printable)
    return st

def fuzzFile(fileName):
    #open read/write binary
    fuzzFile = open(fileName, "r")
    newFile = open(fileName + "_tmp", "w")
    c = fuzzFile.read(1)
    while c != '':
        newFile.write(random.choice(string.printable))
        #jump random amount in file
        for i in range(random.randint(1, 30)):
            c = fuzzFile.read(1)
            if c != '':
                newFile.write(c)
            else:
               print("done")
               break
    fuzzFile.close()
    newFile.close()
    rename(fileName + "_tmp", fileName)
    return fileName


def fuzzArgs(argsList):
    newlist = []
    for arg in argsList:
        val = None
        if arg[0] == 'int':
            val = str(fuzzInt())
        elif arg[0] == 'string':
            val = fuzzString()
        elif arg[0] == 'file':
            val = fuzzFile(arg[1])
        else:
           val = arg[1]
        newlist.append((arg[0], val))
    return newlist

def completeRun(retCode, argList):
    output = open('out.json', 'r')
    outJson = output.read()
    newFlow = ControlFlow()
    newFlow.decode(outJson)
    flowList.append(newFlow)
    if retCode != 0:
        print('Process crash! with args:')
        print(argList)
        newFlow.printCallTree()
    else:
        print('Process completed without issue with args:')
        print(argList)

def printEndRun():
    stats = calcStats(funcList, flowList)
    printStats(stats)

#Takes one command line argument for the file name
def main():
    if len(sys.argv) < 4:
        print('Please provide a file name and run count')
        print('pyFuzz inFile run# \'string, int, static:<arg>, file:<filename>\'')
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

    #run the tooled file multiple times
    argPairs = makeArgs(parmList)
    for i in range(0,runCount):
        argPairs = fuzzArgs(argPairs)
        args = [x[1] for x in argPairs]
        exCode = subprocess.call(["python3", 'tooled_' + inFile] + args)
        completeRun(exCode, args)
    printEndRun()


if __name__ == "__main__":
    main()

