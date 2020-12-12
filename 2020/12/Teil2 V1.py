import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

nav = []
for str in lines:
    str = str.rstrip('\n')
    nav.append((str[0], int(str[1:])))

dirToWind = "ESWN"
windToNorthFactor = {"N": 1, "S": -1, "E": 0, "W": 0}
windToEastFactor = {"N": 0, "S": 0, "E": 1, "W": -1}

dir = 0  # E
pn = 1
pe = 10
shipn = 0
shipe = 0
for c, l in nav:
    if c == 'F':
        # print("ship n/e", shipn, shipe, "wp n/e", pn, pe)
        shipn += l * pn
        shipe += l * pe
        # print('forward:', l, "means n/e", l * pn, l * pe, "to n/e", shipn, shipe)
        continue
    elif c == 'R':
        # print("ship n/e", shipn, shipe, "wp n/e", pn, pe)
        for count in range(0, l // 90):
            (pn, pe) = ((-pe), (pn))
            # print ("turn wp", c, "for", l, "res 1 turn n/e:", pn, pe)
        continue
    elif c == 'L':
        # print("ship n/e", shipn, shipe, "wp n/e", pn, pe)
        for count in range(0, l // 90):
            (pn, pe) = ((pe), (-pn))
            # print ("turn wp", c, "for", l, "res 1 turn n/e:", pn, pe)
        continue

    print("ship n/e", shipn, shipe, "wp n/e", pn, pe)
    if c not in windToNorthFactor:
        raise RuntimeError
    (pn, pe) = (pn + l * windToNorthFactor[c], pe + l * windToEastFactor[c])
    print('move wp:', c, l, 'to wp:', pn, pe)

print("pos & dir:", shipn, shipe, dir, "manh", abs(shipn) + abs(shipe))
# 89936
