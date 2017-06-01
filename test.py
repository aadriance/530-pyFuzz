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
    for i in range(0,2):
        for j in range(0,1):
            if 1:
                pass
            else:
                pass
                return 1
    return 1

def index_find(pattern, string, ignore_case):
    """Find index of pattern match in string. Returns -1 if not found."""
    if ignore_case:
        pattern = pattern.lower()
        string = string.lower()

    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

if __name__ == "__main__":
    main()