import sys
import re

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

four_digits = re.compile("[0-9]{4}")
hair_color = re.compile("([0-9]|[a-f]){6}")
eye_color = re.compile("(amb|blu|brn|gry|grn|hzl|oth)")
passport_id = re.compile("[0-9]{9}")

valids=0
for line in lines:
    data=line.split(' ')
    fields=[ d.partition(':') for d in data ]
    d = dict( [ (d[0],d[2]) for d in fields ] )

    print (d)

    valid=True
    for must in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
        if not(must in d):
            print ('>> key missing: ' + must)
            valid=False
    if not valid: continue
    
    v=d['byr']
    if not four_digits.fullmatch(v):
        print ('>> key byr: format error')
        continue
    if int(v)<1920 or int(v)>2002:
        print ('>> key byr: out of range')
        continue
    
    v=d['iyr']
    if not four_digits.fullmatch(v):
        print ('>> key iyr: format error')
        continue
    if int(v)<2010 or int(v)>2020:
        print ('>> key iyr: out of range')
        continue
    
    v=d['eyr']
    if not four_digits.fullmatch(v):
        print ('>> key eyr: format error')
        continue
    if int(v)<2020 or int(v)>2030:
        print ('>> key eyr: out of range')
        continue

    v=d['hgt']
    if v[-2:] == 'cm':
        h=int(v[:-2])
        if h<150 or h>193:
            print ('>> key hgt cm: range error')
            continue
    elif v[-2:] == 'in':
        h=int(v[:-2])
        if h<59 or h>76:
            print ('>> key hgt in: range error')
            continue
    else:
        print ('>> key hgt: no in, no cm')
        continue

    v=d['hcl']
    if not v[0]==chr(35):
        print ('>> key hcl: no starting hash')
        continue
    if not hair_color.fullmatch(v[1:]):
        print ('>> key hcl: format error after hash')
        continue

    v=d['ecl']
    if not eye_color.fullmatch(v):
        print ('>> key ecl: format error')
        continue
    
    v=d['pid']
    if not passport_id.fullmatch(v):
        print ('>> key pid: format error')
        continue

    print('>>ok')

    valids += 1

print(valids)
