import sys
from controlFlow import *
from fuzzUtil import *
from redbaron import *
import re
import subprocess
import random
import string
from shutil import copyfile
from os import rename

#Written in python 3

#global variables, bc quick software design
funcList = []
flowList = []
ifCount = 0

INTMAX = 4000000



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

def processRedDef(red):
    defList = red.find_all("DefNode")
    for dNode in defList:
        #insert makeControlFlow code
        defName = dNode.name + '('
        if len(dNode.arguments) > 0:
            for arg in dNode.arguments:
                defName += arg.dumps() + ','
            defName = defName[0:-1]
        defName += ')'
        dNode.value.insert(0,"makeControlFlow(\"" + defName + "\")")
        dNode.value.append("exitFunction()")
        funcList.append(dNode.name)
    return red

def processRedIf(red):
    ifList = red.find_all("IfNode")
    global ifCount
    for dNode in ifList:
        testRed = RedBaron("if __name__ == \"__main__\": pass")
        if dNode.test.dumps()==testRed[0].value[0].test.dumps():
            tryLine = 'try:\n'
            for f in funcList:
                tryLine +=  '   registerFunc(\''+ f +'\')\n'
            tryLine += '   ' + dNode.value.dumps().strip()
            tryLine += '\nexcept:\n'
            tryLine += '   print(\'Crash!\')\n   prettyPrint()\n   exit(57)\n'
            dNode.value = tryLine
            print("main try")
        else:
            #insert makeControlFlow code
            ifName = "[" + str(ifCount) + "] if " + dNode.test.dumps()
            ifName = ifName.replace(" ", "_")
            ifCount += 1
            dNode.value.insert(0,"makeControlFlow(\"" + ifName.replace("\"","\\\"") + "\")")
            dNode.value.append("exitFunction()")
            funcList.append(ifName.replace("\"",'''"'''))
    return red

def processRedRet(red):
    retList = red.find_all("ReturnNode")
    for retNode in retList:
        dex = retNode.index_on_parent
        par = retNode.parent
        par.insert(dex, "exitFunction()")
    return red

def processRed(red):
    red = processRedDef(red)
    red = processRedRet(red)
    red = processRedIf(red)
    return red

#Takes one command line argument for the file name
def main():
    if len(sys.argv) < 4:
        print('Please provide a file name and run count')
        print('pyFuzz inFile run# \'string, int, static:<arg>, file:<filename>\'')
        exit(1)
    inFile = sys.argv[1]
    runCount = int(sys.argv[2])
    parmList = sys.argv[3].split(', ')
    outData = open('tooled_' + inFile, 'w')
    #outData = open('tooled_' + inFile, 'a')
    #bring fuzz util into the tooled file
    outData.write('from fuzzUtil import *\n')
    with open(inFile, "r") as source:
        red = RedBaron(source.read())

    red = processRed(red)
    outData.write(red.dumps())
    outData.close()
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

