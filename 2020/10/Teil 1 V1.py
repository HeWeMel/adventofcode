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
print(device)

ints.append(0)
ints.append(device)

dist1count=0
dist3count=0

last=0
distcount3 = 0
distcount1 = 0
for i in sorted(ints):
    print (i)
    d = i - last
    print ('d', d)
    if d == 3:
        distcount3 += 1
        print (3, distcount3)
    if d == 1:
        distcount1 += 1
        print(1, distcount1)
    last = i

print('d1', distcount1)
print('d3', distcount3)
print(distcount1 * distcount3)
