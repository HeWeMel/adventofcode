import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines = '''
13,16,0,12,15,1
'''[1:-1].split('\n')  # split example in lines, keep line endings
# 0,3,6

lastcalled = dict()
round = 1
last = 0
firsttime = False

str = lines[0].rstrip('\n')
for ns in str.split(','):
    n = int(ns)
    if n in lastcalled:
        firsttime = lastcalled[n]
    else:
        firsttime = None
    # last = n
    lastcalled[n] = round
    round += 1
    print(n)

# print("mmm", lastcalled[0])
print()

while round <= 2020:
    print("round", round, ": last number", n, "has firsttime", firsttime)
    if firsttime != None:
        n = round - 1 - firsttime
    else:
        n = 0
    print("speak", n)

    if n in lastcalled:
        firsttime = lastcalled[n]
    else:
        firsttime = None

    print("new firsttime for new n", n, firsttime)
    # last = n
    lastcalled[n] = round
    round += 1
print("lkast:", n)
# 319