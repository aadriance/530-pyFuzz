def data(a):
    a = 4

def test(a,b):
    ret = a
    b = a
    a = ret

def main():
    test(2,3)
    test(3,3)

main()