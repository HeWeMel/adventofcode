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
#print(busses)

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
    # BTW: For the given data, the gcd is 1, since the bus numbers have no common
    # divisor. Thus, the LCM (a,b) is here simply a * b. Bus this is input specific.
    #   jumps = jumps * b
    #print ('step:', b, p, (time+p)%b, jumps)

print (time)
# 702970661767766

#check:
#for n, r in busses:
#    print (n, r, r%n, (time+r) % n)


