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

for s in lines:
    s = s.rstrip('\n')
    op, p = re.split(r" = ", s)
    if op == "mask":
        andm = int( (p.replace('X', '1')), 2)
        orm = int( (p.replace('X', '0')), 2)
    elif op[0:3] == "mem":
        adr=int(op[4:-1])
        c = int(p)
        cn = (c & andm) | orm
        mem[adr] = cn
    else:
        raise RuntimeError()
#print (mem)

s=0
for adr in mem:
   s += mem[adr]
print (s)
#17765746710228