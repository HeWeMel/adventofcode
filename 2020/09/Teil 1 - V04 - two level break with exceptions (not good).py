import sys, itertools, re, functools, operator

with open('input.txt') as f:
    lines = f.readlines()  # read complete file, create list of lines with CRs

ints = []
for line in lines:
    line = str.rstrip(line, '\n')
    if len(line) == 0: continue
    ints.append(int(line))

class MyException(Exception):
    # raise MyException('text')
    def __init__(self, text=''):
        self.text = text

w = 50
for p in range(w, len(ints)):
    try:
        i = ints[p]
        isSum = False
        for (a, b) in itertools.combinations(ints[p - w:p], 2):
            if a + b == i:
                raise MyException()
        print("solution: error at:", i)
        break
    except MyException as e:
        continue
# 258585477
