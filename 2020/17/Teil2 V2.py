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

def printstate(wv, xv, yv, zv, wt, xt, yt, zt):
    na = 0
    for w in range(wv, wt + 1):
        for z in range (zv, zt+1):
            print ("z", z, "w", w, "xv", xv, "yv", yv)
            for y in range (yv, yt+1):
                s = ""
                for x in range (xv, xt+1):
                    s = s + ( "." if state[(w, x, y, z)] == 0 else "#" )
                print (s)
            print()
    print("--------------")
    return na

def sizes():
    na = 0
    wvv = xvv = yvv = zvv = wtt = xtt = ytt = ztt = None

    for (w, x, y, z) in state:
        if state[(w, x, y, z)] == 1:
            na += 1
            if wvv == None or w < wvv:
                wvv = w
            if xvv == None or x < xvv:
                xvv = x
            if yvv == None or y < yvv:
                yvv = y
            if zvv == None or z < zvv:
                zvv = z
            if wtt == None or w > wtt:
                wtt = w
            if xtt == None or x > xtt:
                xtt = x
            if ytt == None or y > ytt:
                ytt = y
            if ztt == None or z > ztt:
                ztt = z
    return na, wvv, xvv, yvv, zvv, wtt, xtt, ytt, ztt

sz = len(lines[0].rstrip('\n'))

w=z=0
for y in range(0, sz):
    #print (y)
    s = lines[y]
    s = s.rstrip('\n')
    for x in range(0, sz):
        i = 0 if s[x] == "." else 1
        state [ (w, x, y, z) ] = i

na, wv, xv, yv, zv, wt, xt, yt, zt = sizes()
#printstate( wv, xv, yv, zv, wt, xt, yt, zt)


diffs = []
for w in range(-1, 2):
    for x in range(-1, 2):
        for y in range(-1, 2):
            for z in range(-1, 2):
                if not (w==0 and x==0 and y==0 and z==0):
                    diffs.append( (w, x, y, z) )

#print ("Diffs", diffs)

def numocc(w, x, y, z):
    numberoccupied = 0
    #print(row, column)
    for (wd, xd, yd, zd) in diffs:
        wc = w + wd
        xc = x + xd
        yc = y + yd
        zc = z + zd
        if state[ (wc, xc, yc, zc) ] == 1:
            numberoccupied += 1
    return numberoccupied

wv = xv = yv = zv = 0
wt = xt = yt = zt = sz - 1
#print(wv, xv, yv, zv, wt, xt, yt, zt)

for cycle in range(0,6): # 6
    modl = []
    for w in range(wv-1, wt+1 +1):
        for x in range(xv-1, xt+1 +1):
            for y in range(yv-1, yt+1 +1):
                for z in range(zv-1, zt+1 +1):
                    a = state[ (w, x, y, z) ]
                    no = numocc( w, x, y, z )
                    #print (w, x, y, z, ":", a, no)
                    if a == 0 and no == 3:
                        modl.append( ((w, x, y, z), 1) )
                    if a == 1 and not (no ==2 or no ==3):
                        modl.append( ((w, x, y, z), 0) )

    for ( (w, x, y, z), m) in modl:
        state[(w, x, y, z)] = m

    na, wv, xv, yv, zv, wt, xt, yt, zt = sizes()
    #print("Sizes:", sizes( wv, xv, yv, zv, wt, xt, yt, zt ))
    #printstate( wv, xv, yv, zv, wt, xt, yt, zt)

print ("res", na)
# 2296