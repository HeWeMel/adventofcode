import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
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

myTicket = [ int(t) for t in re.split(r",", ss[nr]) ]
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

validatedtickets = []
invalid = 0
for ticket in tickets:
    #print(ticket)
    validt = True
    for v in ticket:
        validv = False
        for field, fromtos in rules:
            for f, t in fromtos:
                if v >= f and v <= t:
                    validv = True
        if not validv:
            #print(v)
            invalid += v
            validt = False
    if validt:
        validatedtickets.append(ticket)

print ("inval fields sum", invalid)
validatedtickets.append(myTicket)
print ("val tickets", validatedtickets)
print ("------------")

rulesindexes = [i for i in range(0, len(rules))]
#print ("indexes:", rulesindexes)
for p in itertools.permutations(rulesindexes, len(rules)):
    #print ("fields permutation", p)
    validperm = True
    for i, (label, l)  in zip(itertools.count(0), rules):
        for ticket in validatedtickets:
            validticket = False
            v = ticket[p[i]]
            for f, t in l:  # right side of rule
                if (v >= f and v <= t):
                    validticket = True
                    break
            if not validticket:
                #print("wrong ticket:", ticket)
                #print(">>", v, l)
                validperm = False
                break
        if not validperm:
            break
    if not validperm:
        continue
    print("solution:")
    result=1
    for i, (label, l) in zip(itertools.count(0), rules):
        print (i, (label, l))
        v = myTicket[p[i]]
        print(">>", label, v)
        if label[0:len("departure")] == "departure":
            result *= v
    print ("result", result)
    break
