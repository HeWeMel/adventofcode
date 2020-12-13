import sys
import re
import itertools
import functools
import math

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# generate list of (bus, place in list)
busses = [(int(bus), i) for bus, i in zip(lines[1].rstrip('\n').split(','), itertools.count())
          if bus != 'x']
# print(busses)


# Extended common divisor
# source: https://www.inf.hs-flensburg.de/lang/krypto/algo/euklid.htm#section2
def extgcd(a, b):
    u, v, s, t = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        u, s = s, u - q * s
        v, t = t, v - q * t
    return a, u, v

# Chinese remainder algorithm
# Input format changed to list of (number, remainder). Numbers must have gcd 1 pairwise.
# Output: Product of the moduln, number x according to the chinese remainder theorem.
# source: https://www.inf.hs-flensburg.de/lang/krypto/algo/chinese-remainder.htm
# (parameter changed)
def chineseRemainder(pp):
    if len(pp) == 1:
        return pp[0]
    else:
        k = len(pp) // 2
        m, a = chineseRemainder(pp[:k])
        n, b = chineseRemainder(pp[k:])
        g, u, v = extgcd(m, n)
        x = (b - a) * u % n * m + a
        return m * n, x


cr = chineseRemainder([(n, n - r % n) for n, r in busses])[1]
print(cr)
# 702970661767766

# check:
# for b,r in busses:
#    print (b, r, (cr+r) % b)
