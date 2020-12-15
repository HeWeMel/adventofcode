import collections

# input
nn = [13,16,0,12,15,1]

round, lastcalled = 1, collections.defaultdict( (lambda: None) )

for n in nn:
    prevcalled, lastcalled[n], round = lastcalled[n], round, round + 1

# round = number of next round, n = number last spoken, prevcalled = none or previous round when n has been spoken
while round <= 2020:
    n = 0 if prevcalled == None else (round - 1) - prevcalled
    prevcalled, lastcalled[n], round = lastcalled[n], round, round + 1

print("lkast:", n)
# 319