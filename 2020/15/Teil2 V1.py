# input
s = '13,16,0,12,15,1'
# first example: 0,3,6

lastcalled = dict()

round = 1
for ns in s.split(','):
    n = int(ns)
    # print(n)
    lastcalled[n] = round
    round += 1
if n in lastcalled:
    firsttime = lastcalled[n]
else:
    firsttime = None
# print()

# round = number of next round, n = number last spoken, firsttime = none or round when n has been spoken last before
while round <= 30000000:
    ## choose and speak
    # print("round", round, ": last number", n, "has firsttime", firsttime)
    if firsttime != None:
        n = (round - 1) - firsttime
    else:
        n = 0
    # print("speak", n)

    ## update state
    if n in lastcalled:
        firsttime = lastcalled[n]
    else:
        firsttime = None
    # print ("new firsttime for new n", n, firsttime)
    lastcalled[n] = round
    round += 1
print("lkast:", n)
# 2424