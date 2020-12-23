import sys
import re
import itertools
import functools
import collections


# follow successor function succ from node start till start is reached again, and return string of node names
def listToString(start, succ):
    s = ""
    n = start
    while True:
        s = s + str(n)
        n = succ[n]
        if n == start:
            break
    return(s)


# play the game with input string s, requested size for expanding the input, and the number of rounds to play
def play(s, targetSize, rounds):
    l = [int(i) for i in list(s)]    # string of chars to list of ints
    if sorted(l) != list(range(1, 1 + len(l))):
        print("problem")
        raise RuntimeError("input list is no permutation of the first n numbers")
    m = len(l)  # equal to max(l)

    # Make a circular linked list out of l by calculating successor values for each value. Store them in an array.
    # Extend it to size targetSize.
    succ = (m + 1) * [-1]   # Initialize empty list of nodes. We will not use node 0, the numbers in the data start with 1
    for i in range(m-1):  # for the numbers in the list, except for the last, the successor is the next number in the list
        succ[l[i]] = l[i + 1]  # attention: l is addressed from 0 to m-1
    if m == targetSize:
        succ[l[m - 1]] = l[0]  # the successor of the last number in the list is the first number in the list
    else:
        succ[l[m - 1]] = m + 1  # the successor of the highest number in the list is the first number "after" the list
        succ.extend([i + 1 for i in range(m + 1, targetSize)])  # for further numbers, successor is next number
        succ.append(l[0])  # the successor of the highest number (max) is the first number in the puzzle data

    start = l[0]  # start with the first number in the puzzle data
    for i in range(rounds):  # iterate for the requested number of rounds
        # take our three cups after cup start
        t = []
        for j in range(3):  # for the three next elements
            t.append(succ[start])  # put element to the "taken elements"
            succ[start] = succ[succ[start]]  # remove it from the list (change link from start)
        # insert taken cups after the cup that is next smaller to cup start and is not under the taken cups
        smaller = start
        while smaller == start or smaller in t:
            smaller = (smaller - 1) if smaller > 1 else targetSize  # index of next smaller cup, wrap to max
        succ[t[2]] = succ[smaller]  # insert "taken" list t in whole list after element "smaller"
        succ[smaller] = t[0]
        # from start cup, go one further
        start = succ[start]

    return start, succ


# ------------------ tests and puzzle outputs ----------------

example = "389125467"   # example
puzzle =  "614752839"   # real puzzle data
# start, succ = play(s, targetSize, rounds):

print("--- test part 1 ---")
start, succ = play(example, 9, 10)
s = listToString(start, succ)
print("example data, 10 rounds, resulting list", s, "ok" if s == "837419265" else "failed")
s = listToString(succ[1], succ)[:9-1]
print("example data, 10 rounds, labels after cup 1", s, "ok" if s == "92658374" else "failed")

start, succ = play(puzzle, 9, 100)
labelAfterCup1 = succ[succ[1]]
s = listToString(succ[1], succ)[:9-1]
print("puzzle data, 100 rounds, labels after cup 1, official result", s, "ok" if s == "89372645" else "failed")
print()


print("--- test part 2 ---")
start, succ = play(example, 1000000, 10000000)
l1 = succ[1]
l2 = succ[l1]
p = l1 * l2
print("Example data extended to 1000000, 100 rounds. Resulting numbers and product",
      l1, l2, p, "ok" if p == 149245887792 else "failed")

start, succ = play(puzzle, 1000000, 10000000)
l1 = succ[1]
l2 = succ[l1]
p = l1 * l2
print("Puzzle data extended to 1000000, 10000000 rounds. Resulting official numbers and product",
      l1, l2, p, "ok" if p == 21273394210 else "failed")