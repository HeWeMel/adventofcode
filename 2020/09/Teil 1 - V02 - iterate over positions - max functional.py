import sys, itertools, re, functools, operator

with open('input.txt') as f:
    lines = f.readlines()  # read complete file, create list of lines with CRs

ints = []
for line in lines:
    line = str.rstrip(line, '\n')
    if len(line) == 0: continue
    ints.append(int(line))

w = 50
for p in range(w, len(ints)):
    i = ints[p]
    combis = itertools.combinations(ints[p - w:p], 2)
    if not functools.reduce((lambda a, b: a or b), (a + b == i for (a, b) in combis)):
        print("error:", i)
        break

# 258585477
