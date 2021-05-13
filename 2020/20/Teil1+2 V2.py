import math
import sys

file = 'input.txt'
# For using test input instead of file input comment out following line
# file = 'input_example.txt'
with open(file) as f:
    t = f.read()  # read complete file, results string of lines with endings


print(' -------------- part 1:  -------------- ')
print(' -------------- read in tiles --------------')

def revstr(s):
    return ''.join(reversed(s))  # Reversed returns reversed iterator. Join its results to empty string.


tilesCount = 0
tilesBorder = dict()
tilesPic = dict()
for tile in t.split('\n\n'):  # datasets separated by empty lines, change into list, lines still with endings
    tile = tile.split('\n')  # lines in tile
    tile = [line.rstrip('\n') for line in tile]  # each line without return

    # get name and tile description
    name = tile[0][-5:-1]  # first line contains tile name ("Tile 3557:")
    tilePic = tile[1:]  # the other lines contain the tile

    # get four strings of the border characters, borders read clockwise
    top = tilePic[0]
    bottom = ''.join(reversed(tilePic[-1]))  # last line in reversed order
    left = ''.join(reversed([line[0] for line in tilePic]))  # first column in reversed order
    right = ''.join([line[-1] for line in tilePic])  # last column

    # store results
    tilesCount += 1
    tilesBorder[name] = (top, right, bottom, left)
    tilesPic[name] = tilePic

tilesNoInLine = int(math.sqrt(tilesCount))
print("tileDim", tilesNoInLine)
print()


print('--- configure tiles in TSP_br17 (position, rotation, flip) with, in overlapping, consistent borders ----')

# for each tile in the TSP_br17, store name, rotation, flip and resulting border in dictionaries
tileNameAtPos = dict()
rotAtPos = dict()
flipAtPos = dict()
tileBorderAtPos = dict()


# for a given partial configuration up to previous tile, continue with next tile at tilePos
# with the tiles in tileNames
def configTiles(tilePos, tileNames):
    posY, posX = tilePos // tilesNoInLine, tilePos % tilesNoInLine  # y/x of tile in TSP_br17
    for tileName in tileNames:  # at that position, try each of the given tiles
        t1, r1, b1, l1 = tilesBorder[tileName]
        for rot in range(4):  # try every possible rotation
            if rot > 0:
                t1, r1, b1, l1 = l1, t1, r1, b1  # rotate border once
            for flip in range(2):  # try both without and with vertical flip
                if flip > 0 or rot > 0:
                    t1, r1, b1, l1 = revstr(b1), revstr(r1), revstr(t1), revstr(l1)  # vertical flip border once
                if posX != 0:  # if there is a left neighbor in TSP_br17
                    t2, r2, b2, l2 = tileBorderAtPos[tilePos - 1]
                    if r2 != revstr(l1):  # check, if its right boarder fits my left boarder, both top to bottom
                        ok = False
                        continue
                if posY != 0:  # if there is a neighbor above in TSP_br17
                    t2, r2, b2, l2 = tileBorderAtPos[tilePos - tilesNoInLine]
                    if revstr(b2) != t1:  # check, if its bottom boarder fits my top boarder, both left to right
                        ok = False
                        continue
                # current tile configuration fits, store it to position
                tileNameAtPos[tilePos] = tileName
                tileBorderAtPos[tilePos] = (t1, r1, b1, l1)
                rotAtPos[tilePos] = rot
                flipAtPos[tilePos] = flip
                if tilePos == tilesCount - 1:  # no further tiles to fit in: solution found
                    tl, tr, br, bl = tileNameAtPos[0], \
                                     tileNameAtPos[tilesNoInLine - 1], \
                                     tileNameAtPos[tilesCount - tilesNoInLine], \
                                     tileNameAtPos[tilesCount - 1]
                    print(tl, tr, br, bl)
                    print("res:", int(tl) * int(tr) * int(br) * int(bl))
                    return True
                else:  # further tiles to fit in, try recursively further configuration
                    ok = configTiles(tilePos + 1, [n for n in tileNames if n != tileName])
                    if ok: # return from found complete configuration
                        return ok
    return False

configTiles(0, list(tilesBorder))
print(tileNameAtPos)
# 51214443014783
print()


print('---------------- part 2 ------------------')

tilesSize = len(tilesBorder[list(tilesBorder.keys())[0]][0])  # len(top(first tile))
print("tilesSize", tilesSize)

print('--------- create full picture of the consistent configuration found in part 1 --------')
picture = dict()
for by in range(tilesNoInLine):
    for bx in range(tilesNoInLine):
        tilePos = by * tilesNoInLine + bx
        tileName = tileNameAtPos[tilePos]
        tileRot = rotAtPos[tilePos]
        tileFlip = flipAtPos[tilePos]
        tile = tilesPic[tileName]
        for y in range(tilesSize - 2): # two less, because top and bottom rows are left out
            for x in range(tilesSize - 2):  # two less, because left and right columns are left out
                cx, cy = x + 1, y + 1 # access positions for leaving out top row and left column
                if tileFlip:
                    cx, cy = cx, (tilesSize - 1) - cy # to flip tile vertically, flip get coordinates vertically
                for r in range(tileRot):
                    cx, cy = (tilesSize - 1) - cy, cx  # to rotate tile clockwise, rotate get coordinates ccw
                picture[(by * (tilesSize - 2) + y), (bx * (tilesSize - 2) + x)] = tile[cy][cx] # copy pixel
picDim = tilesNoInLine * (tilesSize - 2) # we left out two pixels of boarder per tile, and have tilesNoInLine of it


def testPrint(picture, picDim):
    for y in range(picDim):
        s = ""
        for x in range(picDim):
            s = s + picture[y, x]
        print(s)
#testPrint(picture, picDim)


print('--------- find monsters --------')

# ------------------
monsterStrings = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "]
monsterHeight, monsterWidth = len(monsterStrings), len(monsterStrings[0])
monsterPosList = [ (y, x) for y in range(3) for x in range(20) if monsterStrings[y][x] == "#" ]
print(monsterPosList)

# try all combinations of rotation and with/without vertical flipping
# of the picture to find any monsters
for rot in range(4):
    for flip in range(2):
        rotPic = dict()
        for px in range(picDim):
            for py in range(picDim):
                cx, cy = px, py
                if flip:
                    cx, cy = cx, (picDim - 1) - cy  # to flip tile vertically, flip get coordinates vertically
                for r in range(rot):
                    cx, cy = (picDim - 1) - cy, cx  # to rotate tile clockwise, rotate get coordinates ccw
                rotPic[(py, px)] = picture[(cy, cx)]

        # search monster in positions in picture, where its dimensions would fit in
        monsterArea = set()
        for px in range(picDim - monsterWidth):
            for py in range(picDim - monsterHeight):
                ok = True
                for my, mx in monsterPosList:
                    if rotPic[(py + my, px + mx)] != "#":
                        ok = False  # no monster here, if expected monster pixel is missing
                        break
                if not ok:
                    continue
                print("monster at", py, px)
                for my, mx in monsterPosList:
                    monsterArea.add((py + my, px + mx))
        if len(monsterArea) > 0:
            print("flip and rot:", flip, rot)
            testPrint(rotPic, picDim)
            print("monster area", len(monsterArea))
            hashArea = len([ (x, y) for x in range(picDim) for y in range(picDim) if rotPic[(y, x)] == "#"])
            print("rest", hashArea - len(monsterArea))
            sys.exit()
# rest 2065
