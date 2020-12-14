import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''[1:-1].split('\n')   # split example in lines, keep line endings

mem=dict()
def getMem(adr):
    if adr in mem:
        return mem[adr]
    else:
        return '00000000000000000000000000000000000'

print()


for s in lines:
    s = s.rstrip('\n')
    #print(len(s))

    op, p = re.split(r" = ", s)
    print (op, p)

    if op == "mask":
        andm = int( (p.replace('X', '1')), 2)
        print(andm)
        orm = int( (p.replace('X', '0')), 2)
        print(orm)
        print()
    elif op[0:3] == "mem":
        adr=int(op[4:-1])
        c = int(p)
        cn = (c & andm) | orm

        #cn = [ 0 if mc=='0' else (1 if mc=='1' else cc) for mc, cc in zip(m, p) ]

        print (s)
        print ("value", c)
        print ("value", '{0:37b}'.format(c))
        print ("mand ", '{0:37b}'.format(andm))
        print ("mor  ", '{0:37b}'.format(orm))
        print ("set  ", '{0:37b}'.format(cn))
        print(cn)
        print()
        mem[adr] = cn
    else:
        raise RuntimeError()

print (mem)

s=0
for adr in mem:
   s += mem[adr]

print (s)
#17765746710228