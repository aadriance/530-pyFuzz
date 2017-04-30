#util functions to be used by the tooled file
import re
from controlFlow import *

def makeControlFlow(inFunc):
    obj = ControlFlow()
    funcDecl = re.split(r'[(, )]', inFunc)

    #sets the descriptor to the name of the function
    #print(funcDecl)
    obj.descriptor = funcDecl[0]

    #first element is the descriptor, rest are parameters, so indexing starts at 1.
    for i in funcDecl[1: len(funcDecl)-1]:
        key = i
        obj.parameters.update({key: None})
    return obj