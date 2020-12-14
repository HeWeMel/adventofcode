import sys
import re
import itertools
import functools
import collections

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

mem = collections.defaultdict(int)      # default factory function int returns 0 for get on nonexistent keys

orm=0           # Just to get rid of IDE warning, that orm might get used uninitialized
floatXors=[]    # Just to get rid of IDE warning, that floatXors might get used uninitialized
for s in lines:
    s = s.rstrip('\n')
    op, p = re.split(r' = ', s)

    if op == "mask":
        # print(op, p)
        orm = int( (p.replace('X', '0')), 2)                            # mask for doing a bitwise "or" on a value
        floatBits = [2**i for i in range(len(p)) if p[-i-1] == 'X' ]    # list of single-bit ints for floating bits

    elif op[0:3] == "mem":
        c = int(p)
        adr1 = int(op[4:-1])
        # print("mem", adr, p)
        adr2 = adr1 | orm                                   # apply or-mask
        for xx in itertools.chain.from_iterable(            # all possible subsets of floatXors, including empty set
                    itertools.combinations(floatBits, r) for r in range(len(floatBits) + 1)):
            adr3 = adr2
            for x in xx:                                    # in adr, change mask bits of chosen subset
                adr3 = adr3 ^ x
            mem[adr3] = c                                   # for all floated addresses, store value to it
    else:
        raise RuntimeError()
#print()

s = sum( mem[adr] for adr in mem )
print (s)
#4401465949086
