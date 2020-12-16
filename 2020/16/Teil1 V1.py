import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesexample='''
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''[1:-1].split('\n')   # split example in lines, keep line endings

ss = []
for s in lines:
    s = s.rstrip('\n')
    ss.append(s)

nr=0

rules = []
while True:
    s = ss[nr]
    nr += 1
    if s == "":
        break
    label,r = re.split(r": ", s)
    rliststr = re.split(r" or ", r)
    rlist = []
    for oner in rliststr:
        l,s,r = oner.partition('-')
        rlist.append( (int(l),int(r)) )
    rules.append( (label, rlist) )
print (rules)

print (ss[nr])
nr += 1

myTicket = re.split(r",", ss[nr])
nr += 1
print ("Ticket:", myTicket)

print (ss[nr])
nr += 1
print (ss[nr])
nr += 1

tickets = []
while nr < len(ss):
    ticket = [ int(t) for t in ss[nr].split(",") ]
    tickets.append(ticket)
    nr += 1
print(tickets)
print()

invalid = 0
for ticket in tickets:
    print(ticket)
    validt = True
    for v in ticket:
        validv = False
        for field, fromtos in rules:
            for f, t in fromtos:
                if v >= f and v <= t:
                    validv = True
        if not validv:
            print(v)
            invalid += v

print (invalid)
