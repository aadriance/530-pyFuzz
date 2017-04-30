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
    if line[0:3] == 'def':
        inFunc = line.replace('def ', '').replace(':\n','')
        line += whiteSpace + 'obj = makeControlFlow(' + inFunc + ')\n'
        line += whiteSpace + 'print(obj.encode())\n'
        callQueue.append(inFunc)
    elif whiteSpaceCount(line, 1) == 1 and len(callQueue) > 0:
        outFunc = callQueue[len(callQueue)-1]
        #line = whiteSpace + 'print(\'Leaving function ' + outFunc + ' \')\n' + line
        callQueue = callQueue[0:len(callQueue)-1]
    prevLine = line
    return line

#Returns the count of leading whitespace
def whiteSpaceCount(line, hi):
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
    #bring fuzz util into the tooled file
    outData.write('from fuzzUtil import *\n')
    for line in inData:
        outData.write(processLine(line))

if __name__ == "__main__":
    main()

