import sys
import re
import itertools
import functools
import math

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

start = int(lines[0])
busses = [int(bus) for bus in lines[1].rstrip('\n').split(',') if bus != 'x']   # leave out busses 'x'
#print("start", start)
#print ("busses", busses)

for time in itertools.count(start):
    for bus in busses:
        if time % bus == 0:
            print("At", time, "take bus", bus, "when waiting was", time - start, "and result is", bus * (time - start))
            sys.exit()
# 2092
