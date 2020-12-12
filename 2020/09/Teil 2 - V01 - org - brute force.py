import sys, itertools
import re

with open('input.txt') as f:
    lines = f.readlines()  # read complete file, create list of lines with CRs

g = 258585477

# create list of ints from the lines
ints = []
for str in lines:
    str = str.rstrip('\n')
    i = int(str)
    ints.append(i)

# solve problem: for all possible sub ranges, check sum (n^3)
for start in range(0, len(ints)):
    for end in range(start, len(ints) - start):
        s = sum(ints[start: end])
        if s == g:
            print(start, end)
            print(min(ints[start: end]) + max(ints[start: end]))
            sys.exit()
# 36981213