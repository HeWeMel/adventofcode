import sys
import re
import itertools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
16
10
15
5
1
11
7
19
6
12
4
'''[1:-1].split('\n')   # split example in lines, keep line endings

ints=[]
for str in lines:
    str = str.rstrip('\n')
    ints.append(int(str))

device=max(ints)+3

ints.append(0)
ints.append(device)


succ=dict()
pred=dict()
for i in ints:
    succ[i] = []
    pred[i] = []

for i in ints:
    for diff in range(1,4):
        if i-diff in ints:
            succ[i-diff].append(i) #,diff
            pred[i].append(i-diff)


ways = dict()
ways[0] = 1

sints = list(sorted(ints))[1:]

for i in sints:
    print (i)
    c = len(pred[i])
    s = 0
    for p in pred[i]:
        if p in ways:
            s += ways[p]
    ways[i] = s

print (ways[device])
# 32396521357312