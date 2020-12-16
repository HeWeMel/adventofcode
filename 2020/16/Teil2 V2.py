import sys
import re
import itertools
import functools
import collections

with open('input.txt') as f:
    lines=f.read()              # read complete file, results string of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines_example='''
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
'''[1:-1]

rule_strings, myticket_string, nbtickets_strings = lines.split('\n\n') # separate datasets at empty lines into list, lines still with endings
rule_strings = rule_strings.split('\n')
myticket_string = myticket_string.split("\n")[1]
nbtickets_strings = nbtickets_strings.split('\n')[1:]

# read rules
rules = []
for s in rule_strings:
    label,r = re.split(r': ', s)
    rliststr = re.split(r' or ', r)
    rlist = []
    for one_r in rliststr:
        l,s,r = one_r.partition('-')
        rlist.append( (int(l),int(r)) )
    rules.append( (label, rlist) )
print ("Rules:", rules)

# read my ticket
myTicket = [ int(t) for t in myticket_string.split(',') ]
print ("Ticket:", myTicket)

# read tickets
tickets = []
for s in nbtickets_strings:
    ticket = [ int(t) for t in s.split(',') ]
    tickets.append(ticket)
print("NB tickets:", tickets)
print('--------------------')

# validate tickets
validatedtickets = []
invalid = 0
for ticket in tickets:
    #print(ticket)
    validt = True
    for v in ticket:
        validv = False
        for field, fromtos in rules:            # value is valid, if it is valid for some range in some rule
            for f, t in fromtos:
                if v >= f and v <= t:
                    validv = True
        if not validv:
            #print(v)
            invalid += v
            validt = False
    if validt:                                  # ticket ist valid, if all fields are valid
        validatedtickets.append(ticket)

print ("inval fields sum", invalid)
validatedtickets.append(myTicket)               # my ticket is valid per definition
print ("val tickets", validatedtickets)
print('--------------------')

# for all labels, store in dictionary the positions, for that
# the values at this position of all the tickets are valid
ticketlen = len(validatedtickets[0])
fits = collections.defaultdict(list)
for i, (label, l) in zip(itertools.count(0), rules):
    for pos in range(ticketlen):
        validpos = True
        for ticket in validatedtickets:
            validticket = False
            v = ticket[pos]
            for f, t in l:  # right side of rule
                if (v >= f and v <= t):
                    validticket = True          # ticket is valid for the rule, if the value is in any of the ranges of the ticket
                    break
            if not validticket:
                #print ("invalid:", label, pos, ticket)
                validpos = False                # chosen pos is invalid, if any ticket is invalid for this choice
                break
        if validpos:
            #print("valid pos", label, pos)
            fits[label].append(pos)             # store pos for label, if valid
print(label, fits)

# calculate recursively:
# How can you assign to the labels of the given rules ticket positions,
# that or none of the forbidden positions and are valid for these labels?
# Returns None if impossible, and tuple of tuples (label, pos) if solution found.
def calc (rules, forbiddenpos):
    (label, l) = rules[0]
    #print(">>", label, setpos)
    for p in fits[label]:
        if p in forbiddenpos:         # p cannot used, it is forbidden
            continue
        if len(rules) == 1:
            return( ((label, p),) )
        res = calc (rules[1:], forbiddenpos + (p,))
        if res != None:       # rekursion erfolgreich
            return( res + ( (label,p), ) )
    return ( None )


rules.sort( key=lambda x: len(fits[x[0]]) )     # sort rules ascending w.r.t. the length of the respective fit list
res=calc (rules, () )                           # start calculation for complete set of rules and no pos used so far
if res == None:
    raise RuntimeError

result = 1
for label, pos in res:
    #print (f, pos)
    v = myTicket[pos]
    print(">>", label, v)
    if label[0:len("departure")] == "departure":
        result *= v                             # if label starts with departure, multiply value of my ticket
print ("result", result)
# 1940065747861
