def ones(n, b = 16):
    return ~n & (2**b - 1)

def twos(n, b = 16):
    return (ones(n, b) + 1) & (2**b - 1)

def neg2twos(n, b = 16):
    if n < 0:
        return twos(-n, b)
    else:
        return n & (2**b - 1)

def twos2neg(n, b = 16):
    if n == 0x8000:
        return -0x8000
    elif n >= (2**(b - 1)):
        return -twos(n, b)
    else:
        return n

def Error(message):
    print(message)
    sys.exit(1)

def parse_int(token):
    if token[:2] == "0x" or token[:3] == "-0x":
        return int(token, 16)
    else:
        return int(token, 10)
