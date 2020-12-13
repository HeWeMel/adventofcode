import sys
import re
import itertools
import functools
import math

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# generate list of (bus, place in list)
busses = [ (int(bus), i) for bus,i in zip( lines[1].rstrip('\n').split(','), itertools.count() )
          if bus != 'x']
print(busses)

# walk through time, first use the time period of the first bus as increment
time = 0
jumps = busses[0][0]
for (b, p) in busses[1:]:     # Leave out first bus. Time and jumps are already given.
    while True:
        if (time+p) % b == 0:
            break
        time += jumps
    # If time fulfils the criteria for the current bus, make the jumps lager and
    # use exactly the length, for that the jumps used so far and the bus period
    # is a divisor, to ensure, that the established relationship for the
    # previous busses an the current bus stays fulfilled. That ist the LCM (least
    # common multiple. LCM (a,b) = abs(a*b) // gcd(a,b) is used to calculate the LCM.
    jumps = abs(jumps * b) // math.gcd(jumps, b)
    #print ('step:', n, b, p, time, jumps)

print (time)
# 702970661767766