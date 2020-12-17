import sys
import re
import itertools
import functools
import collections

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
.#.
..#
###
'''[1:-1].split('\n')   # split example in lines, keep line endings

state = collections.defaultdict( int )

def printstate(xv, yv, zv, xt, yt, zt):
    na = 0
    for z in range (zv, zt+1):
        print ("z", z)
        for y in range (yv, yt+1):
            s = ""
            for x in range (xv, xt+1):
                s = s + ( "." if state[(x, y, z)] == 0 else "#" )
            print (s)
        print()
    print("--------------")
    return na

def sizes(xv, yv, zv, xt, yt, zt):
    na = 0
    xvv = yvv = zvv = xtt = ytt =  ztt = None

    for z in range (zv-1, zt+1+1):
        for y in range (yv-1, yt+1+1):
            for x in range (xv-1, xt+1+1):
                if state[(x, y, z)] == 1:
                    na += 1
                    if xvv == None or x < xvv:
                        xvv = x
                    if yvv == None or y < yvv:
                        yvv = y
                    if zvv == None or z < zvv:
                        zvv = z
                    if xtt == None or x > xtt:
                        xtt = x
                    if ytt == None or y > ytt:
                        ytt = y
                    if ztt == None or z > ztt:
                        ztt = z
    return na, xvv, yvv, zvv, xtt, ytt, ztt

sz = len(lines[0].rstrip('\n'))

z=0
for y in range(0, sz):
    #print (y)
    s = lines[y]
    s = s.rstrip('\n')
    for x in range(0, sz):
        i = 0 if s[x] == "." else 1
        state [ (x, y, z) ] = i

printstate (0, 0, 0, sz-1, sz-1, sz-1)

#print('before')
#for row in range(0,rows):
#    print(seats[row])
#print()

diffs = []
for x in range(-1, 2):
    for y in range(-1, 2):
        for z in range(-1, 2):
            if not (x==0 and y==0 and z==0):
                diffs.append( (x, y, z) )

print (diffs)

def numocc(x, y, z):
    numberoccupied = 0
    #print(row, column)
    for (xd, yd, zd) in diffs:
        xc = x + xd
        yc = y + yd
        zc = z + zd
        if state[ (xc, yc, zc) ] == 1:
            numberoccupied += 1
    return numberoccupied

xv = yv = zv = 0            # min
xt = yt = zt = sz - 1       # max coord
print(xv, yv, zv, xt, yt, zt)

for cycle in range(0,6):
    modl = []
    for x in range(xv-1, xt+1 +1):
        for y in range(yv-1, yt+1 +1):
            for z in range(zv-1, zt+1 +1):
                a = state[ (x, y, z) ]
                no = numocc( x, y, z )
                print (x, y, z, ":", a, no)
                if a == 0 and no == 3:
                    modl.append( ((x, y, z), 1) )
                if a == 1 and not (no ==2 or no ==3):
                    modl.append( ((x, y, z), 0) )

    for ( (x, y, z), m) in modl:
        state[(x, y, z)] = m

    na, xv, yv, zv, xt, yt, zt = sizes( xv, yv, zv, xt, yt, zt )
    print(">>>>>>>>>>>", sizes( xv, yv, zv, xt, yt, zt ))
    printstate( xv, yv, zv, xt, yt, zt)
    #print(state[ (2, 1, 0) ])
    #sys.exit()

print ("res", na)
# 395