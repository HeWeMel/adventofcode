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

# solve problem: slide window over the numbers (n), move start or end if sum does not fit (-> n^2)
window = []
while True:
    s = sum(window)
    if s < g:
        window.append(ints.pop(0))
    elif s > g:
        window.pop(0)
    else:
        print(min(window) + max(window))
        break
# 36981213