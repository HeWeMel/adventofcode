import sys
import re
import itertools
import functools
import math

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesexample='''
939
7,13,x,x,59,x,31,19
'''[1:-1].split('\n')   # split example in lines, keep line endings

#wait = int(lines[0].rstrip('\n'))

busses=[]
start = int(lines[0])
for bus in lines[1].rstrip('\n').split(','):
    if bus == 'x':
        continue
    #print(bus)
    busses.append(int(bus))
#print()

time=start
while True:
    #print(time)
    for bus in busses:
        if time % bus == 0:
            print("At", time, "take bus", bus, "when waiting was", time-start, "and result is", bus * (time-start))
            sys.exit()
    time += 1
# 2092