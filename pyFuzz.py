import sys
from controlFlow import *
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
    if line[0:3] == 'def':
        obj = ControlFlow()
        inFunc = line.replace('def ', '').replace(':\n','')
        funcDecl = re.split(r'[(,)]', inFunc)

        #sets the descriptor to the name of the function
        print(funcDecl)
        obj.descriptor = funcDecl[0]

        #first element is the descriptor, rest are parameters, so indexing starts at 1.
        for i in funcDecl[1: len(funcDecl)-1]:
            key = i
            obj.parameters.update({key: None})

        print(obj.encode())

        line += whiteSpace + 'print(\'In function ' + inFunc + ' \')\n'
        callQueue.append(inFunc)
    elif whiteSpaceCount(line) == 1 and len(callQueue) > 0:
        outFunc = callQueue[len(callQueue)-1]
        line = whiteSpace + 'print(\'Leaving function ' + outFunc + ' \')\n' + line
        callQueue = callQueue[0:len(callQueue)-1]
    prevLine = line
    return line

#Returns the count of leading whitespace
def whiteSpaceCount(line):
    return len(line) - len(line.lstrip())

#Reads the file until it find a line with whitespace
#Records the whitespace so we can replicate it later
def findWhiteSpace(inFile):
    inData = open(inFile, 'r')
    global whiteSpace
    for line in inData:
        if len(line.lstrip()) != len(line) and len(line.lstrip()) != 0:
            for c in line:
                if c.isspace():
                    whiteSpace += c
                else:
                    return
            return

#Takes one command line argument for the file name
def main():
    inFile = sys.argv[1]
    findWhiteSpace(inFile)
    inData = open(inFile, 'r')
    outData = open('tooled_' + inFile, 'a')
    for line in inData:
        outData.write(processLine(line))

if __name__ == "__main__":
    main()

