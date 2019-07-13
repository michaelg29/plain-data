def padNumber(n, length):
    ret = str(n)
    ret = '0' * (length - len(ret)) + ret
    return ret