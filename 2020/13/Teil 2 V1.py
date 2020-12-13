import sys
import re
import itertools
import functools
import math

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesexample = '''
939
7,13,x,x,59,x,31,19
'''[1:-1].split('\n')  # split example in lines, keep line endings

# generate list of (bus, place in list)
busnr = 0
plusses = dict
busses = []
for bus in lines[1].rstrip('\n').split(','):
    if bus != "x":
        busi = int(bus)
        busses.append( (busi, busnr) )
        #print(busi, more)
    busnr += 1
#print()

# walk through time, first with jumps with a lenght of the time period of the first bus
time = 0
jumps = busses[0][0]
for n in range(1, len(busses)):
    (b, p) = busses[n]
    while True:
        if (time+p) % b == 0:
            break
        time += jumps
    # if time fulfils the criteria for the current bus, make the jumps lager and
    # use exactly the length, for that the jumps used so far and the bus period
    # is a divisor, to ensure, that the established relationship for the
    # previous busses an the current bus stays fulfilled. That ist the LCM (least
    # common multiple. LCM (a,b) = abs(a*b) // gcd(a,b) is used to calculate the LCM.
    jumps = abs(jumps * b) // math.gcd(jumps, b)
    #print ('step:', n, b, p, time, jumps)

print (time)
#for n in range(0, len(busses)):
#    (b, p) = busses[n]
#    print ("check:", n, b, p, time + p, (time + p)%b )

# 702970661767766