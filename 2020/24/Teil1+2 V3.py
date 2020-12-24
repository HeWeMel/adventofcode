import collections
import sys

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# ---------- part 1 --------------

# The fact, that the tiles are hexagons and each of them has six neighbors, is reflected as follows:
# - The tiles are horizontally (x axis) numbered in steps of 2 and vertically (y axis) with steps of 1.
# - For rows with even rows numbers, the horizontally numbering starts with 0 and in odd row number with 1.
# Example layout:
#  X X X
# X X X X

# For each move between tiles, the following dict gives the resulting change in coordinates (x, y).
# Horizontal moves make x-steps by two, and diagonal moves make one y- and one x-step.
move = {'e': (2, 0), 'w': (-2, 0), 'nw': (-1, 1), 'ne': (1, 1), 'sw': (-1, -1), 'se': (1, -1)}

# At the beginning, there are no black tiles
blackTiles = set()
def flipTile(pos):
    if pos in blackTiles:
        blackTiles.remove(pos)
    else:
        blackTiles.add(pos)

for s in lines:  # for each list of commands
    s = list(s.rstrip('\n'))    # commands in list of chars
    x, y = 0, 0  # start at this tile position
    while len(s) > 0:   # go through the commands
        c = s.pop(0) if s[0] in move else s.pop(0)+s.pop(0)  # get a one or two character move command
        dx, dy = move[c]  # get coordinate difference that the command should result in
        x, y = x + dx, y + dy  # make those steps
    flipTile((x, y))  # flip tile at end position of the walk
print("part1:", len(blackTiles))
#  411


# ---------- part 2 --------------
diffs = list(iter(move.values()))   # all (x, y) steps that any of the moves can result in
for day in range(100):
    tiles = blackTiles.copy()  # calculate set of tile positions, where tile is black itself or ...
    for (x, y) in blackTiles:
        for xd, yd in diffs:
            tiles.add((x + xd, y + yd))  # ... tile at that position has at least one black neighbor.
    flipTiles = []
    for (x, y) in tiles:    # iterate through those tile positions, because for them, flipping might occur
        blackNeighbors = len([1 for xd, yd in diffs if (x + xd, y + yd) in blackTiles])  # number of black neighbors
        if (blackNeighbors == 0 or blackNeighbors > 2) if (x, y) in blackTiles else blackNeighbors == 2:
            flipTiles.append((x, y))  # if, according to flipping rules, tile has to be flipped, store it in a list
    for (x, y) in flipTiles:    # flip the tiles in the list
        flipTile((x, y))
print("part2:", len(blackTiles))
#  4092