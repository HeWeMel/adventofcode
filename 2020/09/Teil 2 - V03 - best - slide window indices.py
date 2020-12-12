import sys, itertools
import re

with open('input.txt') as f:
    lines = f.readlines()  # read complete file, create list of lines with CRs

g = 258585477

# create list of ints from the lines
ints = []
for str in lines:
    str = str.rstrip('\n')
    i = int(str)
    ints.append(i)

# solve problem: slide window over the numbers (n), move start or end if sum does not fit,
# just change first/last element in indices and sum
s = 0
window_low = 0
window_high = 0
while True:
    if s < g: # sum to low, take next int into window und sum
        i = ints[window_high]
        window_high += 1
        s += i
    elif s > g: # sum to high, remove first int from window and sum
        i = ints[window_low]
        window_low += 1
        s -= i
    else:
        print(
            min(ints[window_low:window_high]) +
            max(ints[window_low:window_high]))
        break
# 36981213