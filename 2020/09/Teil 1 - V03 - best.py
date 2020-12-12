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
    isSum = False
    for (a, b) in itertools.combinations(ints[p - w:p], 2):
        if a + b == i:
            isSum = True
            break
    if not isSum:
        print("solution: error at:", i)
        break

# 258585477
