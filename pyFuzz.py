import sys
from controlFlow import *
from fuzzUtil import *
import re

#Written in python 3

#global variables, bc quick software design
whiteSpace = ''
callQueue = []
prevLine = ''

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
            line = mainspace + 'try:\n' + mainspace + origLine + '\n' + mainspace + 'except:\n' +\
               (mainspace*2) + 'exitFunction()\n'
        else:
            #line comes from earlier if statement. replacing the value here to add try/except
            line = whiteSpace + 'exitFunction()\n'
            line += 'try:\n' + whiteSpace + origLine + '\n' + 'except:\n' + whiteSpace + 'exitFunction()\n'

    elif isFunc(origLine):
        inFunc = origLine.replace('def ', '').replace(':\n','')
        #close function
        line += whiteSpace + 'makeControlFlow(\'' + inFunc.replace('\'', '\\\'') + '\')\n'
        callQueue.append(inFunc)

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

#Takes one command line argument for the file name
def main():
    inFile = sys.argv[1]
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

if __name__ == "__main__":
    main()

