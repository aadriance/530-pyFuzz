def data(a):
    a = 4

def test(a,b):
    ret = a
    b = a
    a = ret
    if 0:
        return 2
    elif 0 == 1:
        return 3
    elif 0==3:
        if 5:
            return 5
        else:
            return -1
    else:
        return 4
    return 2

def main():
    test(2,3)
    test(3,3)
    if 1==1:
        print("wut")

if __name__ == "__main__":
    main()