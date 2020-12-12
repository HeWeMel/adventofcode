import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

nav=[]
for str in lines:
    str = str.rstrip('\n')
    nav.append( ( str[0], int(str[1:]) ) )

dirToWind = "ESWN"
windToNorthFactor = { "N": 1, "S": -1, "E": 0, "W": 0 }
windToEastFactor = { "N": 0, "S": 0, "E": 1, "W": -1 }

dir=0     # E
pn=pe=0
for c, l in nav:
    if c == 'F':
        c=dirToWind[dir]   # for "forward", calc from dir number to wind direction
        #print('forward means:', c)
    elif c=='R':
        #print("turn", c, "for", l, "from", dir)
        dir = (dir + (l//90) ) % 4
        #print ("turn to:", dir)
        continue
    elif c=='L':
        #print("turn", c, "for", l, "from", dir)
        dir = (dir + 4-(l//90) ) % 4
        #print ("turn to:", dir)
        continue

    #print('move:', c, l)
    if c not in windToNorthFactor: raise RuntimeError
    (pn, pe) = (pn + l * windToNorthFactor[c], pe + l * windToEastFactor[c] )
    #print(pn, pn2, pe, pe2)

print("pos & dir:", pn, pe, dir, "manh", abs(pn)+abs(pe))

# 1838