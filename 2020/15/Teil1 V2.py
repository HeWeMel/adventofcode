import collections

# input
s = '13,16,0,12,15,1'

lastcalled = collections.defaultdict( (lambda: None) )

round = 1
for ns in s.split(','):
    n = int(ns)
    prevcalled, lastcalled[n], round = lastcalled[ int(ns) ], round, round + 1

# round = number of next round, n = number last spoken, prevcalled = none or previous round when n has been spoken
while round <= 2020:
    n = 0 if prevcalled == None else (round - 1) - prevcalled
    prevcalled, lastcalled[n], round = lastcalled[n], round, round + 1

print("lkast:", n)
# 319