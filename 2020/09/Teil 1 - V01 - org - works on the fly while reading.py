import sys, itertools
import re

with open('input.txt') as f:
    lines = f.readlines()  # read complete file, create list of lines with CRs

n = []
pr = 50
p = 1
for str in lines:
    str = str.rstrip('\n')
    i = int(str)
    if (p > pr):
        combis = itertools.combinations(n[-pr:], 2)
        ok = False
        for (a, b) in combis:
            if a + b == i:
                ok = True
                break
        if not ok:
            print("error:", i)
            break
    p = p + 1
    n.append(i)
# 258585477
