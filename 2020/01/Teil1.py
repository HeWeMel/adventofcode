with open('input.txt') as f:

    vals = [int(line) for line in f]

    for v in vals:
        rest=2020-v
        if rest in vals:
            print(v*rest)
            break
