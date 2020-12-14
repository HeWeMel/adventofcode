import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''[1:-1].split('\n')   # split example in lines, keep line endings

mem=dict()
def getMem(adr):
    if adr in mem:
        return mem[adr]
    else:
        return '00000000000000000000000000000000000'

print()


def seatToCode(s):
    if len(s) == 1:
        return 1 if s[0] == '1' else 0
    else:
        return seatToCode(s[:-1]) * 2 + seatToCode(s[-1])

def do_floor( ss, m):
    print ("ss", ss)
    print ("m", m)
    for pos in range(0, len(m)):
        if m[pos] == 'X':
            print("found", pos)
            mn = m[0:pos] + "0" + m[pos+1:]
            ssn=[]
            for s in ss:
                sn = s[0:pos] + ("0" if s[pos]=="1" else "1") + s[pos+1:]
                ssn.append(sn)
                #print("newstr ", sn)
            print("newmask", m)
            print("newstrings", ss+ssn)
            return( do_floor(ss+ssn, mn))
    return ss

for s in lines:
    s = s.rstrip('\n')
    #print(len(s))

    op, p = re.split(r" = ", s)
    print (op, p)

    if op == "mask":
        floatmask = p
        #floatand = p.replace('0', '1').replace('{}')
        #floator = p.replace('1', '0').replace('{}')
        #print(andm)
        orm = seatToCode(p.replace('X', '0'))
        #print(orm)
        #print()
    elif op[0:3] == "mem":
        adr=int(op[4:-1])
        c = int(p)
        adrn = adr | orm

        print ("value", '{0:36b}'.format(adr))
        print ("mor  ", '{0:36b}'.format(orm))
        print ("adrn ", '{0:36b}'.format(adrn))
        print(adrn)
        print()

        print (floatmask)
        adrns = '{0:36b}'.format(adrn).replace(" ", "0")
        print (adrns)
        for astr in do_floor( [ adrns ], floatmask):
            print ("astr", astr)
            a=int(astr)
            mem[a] = c
    else:
        raise RuntimeError()

print (mem)

s=0
for adr in mem:
   s += mem[adr]

print (s)