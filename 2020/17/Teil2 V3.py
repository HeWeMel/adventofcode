import sys
import re
import itertools
import functools
import collections

# read input
with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

state = collections.defaultdict( int )
sz = len(lines[0].rstrip('\n'))
w=z=0
for y in range(0, sz):
    #print (y)
    s = lines[y]
    s = s.rstrip('\n')
    for x in range(0, sz):
        i = 0 if s[x] == "." else 1
        state [ (w, x, y, z) ] = i
dimensions = 4


# print state
def printstate(ranges_from, ranges_to):
    for w in range(ranges_from[0], ranges_to[0]+1):
        for z in range (ranges_from[3], ranges_to[3]+1):
            print ("Content for w", w, "z", z, ":")
            for y in range (ranges_from[2], ranges_to[2]+1):
                s = ""
                for x in range (ranges_from[1], ranges_to[1]+1):
                    s = s + ( "." if state[(w, x, y, z)] == 0 else "#" )
                print (s)
    print("--------------")


# utility functions
def elementwise_min(v, w):              # elementwise min of two vectors
    return itertools.starmap(min, zip(v, w))
def elementwise_max(v, w):              # elementwise max of two vectors
    return itertools.starmap(max, zip(v, w))
def elementwise_plus(v, w):             # elementwise sum of two vectors
    return itertools.starmap(sum, zip(v, w))

def sizes():                            # list of min and list of max coordinates in state keys with state content 1
    return len( [key for key in state.keys() if state[key] == 1] ),\
        [ coords for coords in functools.reduce( elementwise_min, [key for key in state.keys() if state[key] == 1] ) ],\
        [ coords for coords in functools.reduce( elementwise_max, [key for key in state.keys() if state[key] == 1] ) ]

# process data
zero_vector = dimensions*(0,)           # vector of zeros of needed dimension
diffs = [diffvector for diffvector in   # all vectors "around" zero vector, without the zero vector itself
         itertools.product(range(-1, 2), repeat=dimensions) if diffvector != zero_vector]

na, mins, maxs = sizes()                # number of elements in state with content 1, vectors of min and max of used range in state

for cycle in range(0,6): # 6
    modl = []
    # iterate the state matrix, with 1 less at the range mins and 1 more at the range max
    ranges = [ [p for p in range(min_val-1, max_val+2)] for (min_val, max_val) in  zip(mins, maxs) ]
    for pos in itertools.product( *ranges ):
        a = state[pos]
        neighbors = [ tuple([np for np in map(sum, zip(pos, d))]) for d in diffs ]  # pos+d for all d in diffs
        no = len( [np for np in neighbors if state[np] == 1] )      # number of neighbor fields with content 1
        # apply rules for changing state, generate modification list
        if a == 0 and no == 3:
            modl.append( (pos, 1) )
        if a == 1 and not (no ==2 or no ==3):
            modl.append( (pos, 0) )

    # apply calculated changes in state
    for (pos, m) in modl:
        state[pos] = m

    # recalculate size of used part of state
    na, mins, maxs = sizes()

print ("res", na)
# 2296