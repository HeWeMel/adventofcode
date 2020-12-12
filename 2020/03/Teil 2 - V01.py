import sys

lines=[]
with open('input.txt', 'r') as f:
    for line in f:
        lines.append(line[:-1]) # remove new line char

l=len(lines)
w=len(lines[0])

r=1
for (sr,sd) in [ (1,1), (3,1), (5,1), (7,1), (1,2) ]:

    z,s=(0,0)
    t=0
    while (z<l):
        print (z, s)
        if lines[z][s%w] == '#':
            t+=1
        z,s=(z+sd, s+sr)
    print (t)
    r=r*t

print (r)
# 2608962048