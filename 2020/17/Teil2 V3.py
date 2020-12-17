import sys
import itertools

# read input
with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings


state = set()
sz = len(lines[0].rstrip('\n'))
w = z = 0
for y in range(0, sz):
    s = lines[y]
    s = s.rstrip('\n')
    for x in range(0, sz):
        if s[x] == "#":
            state.add( (w, x, y, z) )
dimensions = 4

'''
# print state (used only for debugging)
def printstate(ranges_from, ranges_to):
    print ( ranges_from, ranges_to)

    for w in range(ranges_from[0], ranges_to[0] + 1):
        for z in range(ranges_from[3], ranges_to[3] + 1):
            print("Content for w", w, "z", z, ":")
            for y in range(ranges_from[2], ranges_to[2] + 1):
                s = ""
                for x in range(ranges_from[1], ranges_to[1] + 1):
                    s = s + ("." if (w, x, y, z) in state else "#")
                print(s)
    print("--------------")
'''

def sizes():
    # for state keys with state content 1: length, vector of min and of max coordinates
    occupiedStates = list(state)
    return len(occupiedStates), list(map(min, zip(*occupiedStates))), list(map(max, zip(*occupiedStates)))


# process data
zero_vector = dimensions * (0,)  # vector of zeros of needed dimension
diffs = [diffvector for diffvector in  # all vectors "around" zero vector, without the zero vector itself
         itertools.product(range(-1, 2), repeat=dimensions)
         if diffvector != zero_vector]

na, mins, maxs = sizes()  # for state elements with content 1: count, vectors of min and of max coordinates

for cycle in range(0, 6):  # 6
    addl = set()
    removel = set()
    # iterate the state matrix, with 1 less at the range mins and 1 more at the range max
    ranges = [list(range(min_val - 1, max_val + 2)) for (min_val, max_val) in zip(mins, maxs)]
    for pos in itertools.product(*ranges):
        a = (pos in state)
        neighbors = [tuple(map(sum, zip(pos, d))) for d in diffs]  # pos+d for all d in diffs
        no = len([np for np in neighbors if np in state])  # number of neighbor fields with content 1
        # apply rules for changing state, generate modification list
        if not a and no == 3:
            addl.add(pos)
        if a and not (no == 2 or no == 3):
            removel.add(pos)
    # apply calculated changes in state
    state = state.union(addl)
    state = state.difference(removel)
    # recalculate size of used part of state
    na, mins, maxs = sizes()


print("res", na)
# 2296
