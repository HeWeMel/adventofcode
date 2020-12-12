import sys

lines=[]
new=True
lc=0
with open('input.txt', 'r') as f:
    for line in f:
        line=line[:-1] # remove new line char
        if line=='':
            lc+=1
            new=True
        else:
            if new:
                lines.append(line)
                new=False
            else:
                lines[lc] = lines[lc] + " " + line

valids=0
for line in lines:
    valid=True
    for must in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
        if line.find(must)==-1:
            valid=False
    if valid:
        valids += 1

print(valids)

