from fuzzUtil import *
import traceback
def data(a):
    makeControlFlow("data(a)")
    a = 4

    exitFunction()
def test(a,b):
    makeControlFlow("test(a,b)")
    ret = a
    b = a
    a = ret
    if 0:
        makeControlFlow("[0]_if_0")
        exitFunction()
        return 2
        exitFunction()
    elif 0 == 1:
        makeControlFlow("[0]_else_if_0_==_1")
        exitFunction()
        return 3
        exitFunction()
    elif 0==3:
        makeControlFlow("[0]_else_if_0==3")
        if 5:
            makeControlFlow("[1]_if_5")
            exitFunction()
            return 5
            exitFunction()
        else:
            makeControlFlow("[1]_else")
            exitFunction()
            return -1
            exitFunction()
        
        exitFunction()
    else:
        makeControlFlow("[0]_else")
        exitFunction()
        return 4
        exitFunction()
    exitFunction()
    return 2

    exitFunction()
def main():
    makeControlFlow("main()")
    test(2,3)
    test(3,3)
    YouAreNOtReal()

    exitFunction()
if __name__ == "__main__":
    try:
       registerFunc('data')
       registerFunc('test')
       registerFunc('main')
       registerFunc('[0]_if_0')
       registerFunc('[0]_else_if_0_==_1')
       registerFunc('[0]_else_if_0==3')
       registerFunc('[0]_else')
       registerFunc('[1]_if_5')
       registerFunc('[1]_else')
       main()
       prettyPrint()
    
    except:
       print('Crash!')
       print(traceback.format_exc())
       prettyPrint()
       exit(57)
