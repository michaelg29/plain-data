"""
    utils class
""" 

import datetime

"""
    pad number to a certain length
"""
def padNumber(n, length):
    ret = str(n)
    ret = '0' * (length - len(ret)) + ret
    return ret

"""
    get current date as string
"""
def getDate():
    now = datetime.datetime.now()
    month = padNumber(now.month, 2)
    day = padNumber(now.day, 2)
    year = padNumber(now.year, 4)

    return f"{month}/{day}/{year}"