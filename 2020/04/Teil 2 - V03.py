import sys
import re

with open('input.txt', 'rt') as f:
    t=f.read()              # ganze Datei lesen
lines=t.split('\n\n')       # Leere Zeilen sind die Trennung zwischen Pässen

four_digits = re.compile("[0-9]{4}")
hair_color = re.compile("([0-9]|[a-f]){6}")
eye_color = re.compile("(amb|blu|brn|gry|grn|hzl|oth)")
passport_id = re.compile("[0-9]{9}")

valids=0
for line in lines:
    line = line.replace('\n', ' ')              # Mehrzeilige Daten zu einer Zeile machen
    
    data=line.split(' ')                        # Durch Leerzeichen getrennte Angaben
    fields=[ d.partition(':') for d in data ]   # Je Angabe aufteilen in Key, Doppelpunkt, Value
    d = dict( [ (d[0],d[2]) for d in fields ] ) # Key und Value einer Angabe ablegen in dictionary

    print (d)

    valid=True
    for must in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']:
        if not(must in d):
            print ('>> key missing: ' + must)
            valid=False
    if not valid: continue

    def is_year_ok(d, k, l, h):
      v=d[k]
      if not four_digits.fullmatch(v):
          print (f'>> key {k}: format error')
          return False
      if int(v)<l or int(v)>h:
          print ('>> key {k}: out of range')
          return False
      return True
    
    if not is_year_ok(d, 'byr', 1920, 2002): continue
   
    if not is_year_ok(d, 'iyr', 2010, 2020): continue

    if not is_year_ok(d, 'eyr', 2020, 2030): continue

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
# 179
