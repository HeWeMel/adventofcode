import sys

with open('input.txt') as f:

    vals = [int(line) for line in f]

    n=len(vals)
    for i1 in range(n):
        for i2 in range(i1+1, n):
            for i3 in range(i2+1, n):
                if vals[i1]+vals[i2]+vals[i3] == 2020:
                    print(vals[i1]*vals[i2]*vals[i3])
                    sys.exit()
