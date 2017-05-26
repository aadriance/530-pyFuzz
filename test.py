def data(a):
    a = 4

def test(a,b):
    ret = a
    b = a
    a = ret
    if 0:
        return 2
    return 2

def main():
    test(2,3)
    test(3,3)

if __name__ == "__main__":
    main()