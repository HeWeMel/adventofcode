import sys

with open('input.txt', 'r') as f:
    lines=f.readlines()
lines = [ line[:-1] for line in lines ]

def seatToCode (s):
    if len(s) == 1:
        return 1 if s[0]=='B' or s[0]=='R' else 0
    else:
        return seatToCode(s[:-1]) * 2 + seatToCode(s[-1])

d=dict()
l=[]

for line in lines:
    id=seatToCode(line)
    d[id] = line
    l.append(id)

print(max(l))

for id in range(min(l), max(l)):
    if not id in d:
        print(id)
