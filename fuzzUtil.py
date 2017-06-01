#util functions to be used by the tooled file
import re
from controlFlow import *

ObjectStack = []
FuncNames = []


#create object for current function context, 
#add object to previous contect call list, change context
def makeControlFlow(inFunc):
    global ObjectStack
    obj = ControlFlow()
    #if inFunc[0] != "[" or inFunc[2] != "]": 
    funcDecl = re.split(r'[(, )]', inFunc)

    #sets the descriptor to the name of the function
    #print(funcDecl)
    obj.descriptor = funcDecl[0]

    #first element is the descriptor, rest are parameters, so indexing starts at 1.
    for i in funcDecl[1: len(funcDecl)-1]:
        key = i
        obj.parameters.update({key: None})
    if(len(ObjectStack) > 0):
        ObjectStack[len(ObjectStack) - 1].flowTrace.append(obj)
    ObjectStack.append(obj)
    return obj

#pop current context off stack
def exitFunction():
    global ObjectStack
    if(len(ObjectStack) == 1):
        prettyPrint()
    ObjectStack = ObjectStack[0:-1]

def prettyPrint():
    #ObjectStack[0].printCallTree()
    #print('')
    #ObjectStack[0].printStats(FuncNames)
    print("going out")
    outData = open('out.json', 'w')
    outData.write(ObjectStack[0].encode())
    outData.close()
    #print(ObjectStack[0].encode())

def registerFunc(name):
        FuncNames.append(re.split(r'[(, )]', name)[0])


