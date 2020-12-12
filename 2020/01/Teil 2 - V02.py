import itertools

with open('input.txt') as f:

    vals = (int(line) for line in f)

    for (v1,v2,v3) in itertools.permutations(vals, 3):
        if v1+v2+v3 == 2020:
            print(v1, v2, v3, ": ", v1*v2*v3)
            break
