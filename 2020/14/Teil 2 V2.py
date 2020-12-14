import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

mem=dict()
def getMem(adr):
    if adr in mem:
        return mem[adr]
    else:
        return '00000000000000000000000000000000000'

def do_float( ss, m):
    for pos in range(0, len(m)):
        if m[pos] == 'X':
            # at first position in mask string with character X
            mn = m[0:pos] + "0" + m[pos+1:]
            # replace the X by something else ("this X is done" for the recursion)
            ssn=[]
            # create new strings from the given strings, where, at the position
            # of the X in the mask, the bit is flipped from 0 to 1 or from 1 to 0 respectively
            for s in ss:
                sn = s[0:pos] + ("0" if s[pos]=="1" else "1") + s[pos+1:]
                ssn.append(sn)
            return( do_float(ss+ssn, mn))
    return ss

for s in lines:
    s = s.rstrip('\n')

    op, p = re.split(r" = ", s)

    if op == "mask":
        print(op, p)
        floatmask = p
        orm = int( (p.replace('X', '0')), 2)                # mask for doing an bitwise or on a value
    elif op[0:3] == "mem":
        adr=int(op[4:-1])
        c = int(p)
        print("mem", adr, p)
        adrn = adr | orm                                    # the or effect of the mask can be done in binary
        adrns = '{0:36b}'.format(adrn).replace(" ", "0")    # address to binary padded with space, space to "0"
        for astr in do_float( [ adrns ], floatmask):        # floating is done in function
            mem[int(astr)] = c                              # for all floated addresses, store value to it
    else:
        raise RuntimeError()
print()

s=0
for adr in mem:
   s += mem[adr]
print (s)
#4401465949086
