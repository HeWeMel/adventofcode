with open('input.txt') as f:
    t=f.read()              # read complete file, results string of lines with endings

# For using test input instead of file input rename from tx to t
# test for normal game
tx='''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''[1:-1]

# test for recursion stop
tx='''
Player 1:
43
19

Player 2:
2
29
14
'''[1:-1]


part1, part2 = t.split('\n\n')

deck1 = []
deck2 = []
for line in part1.split('\n')[1:]:
    line = line.rstrip('\n')  # lines in block
    deck1.append(int(line))
for line in part2.split('\n')[1:]:
    line = line.rstrip('\n')  # lines in block
    deck2.append(int(line))

game = 0
def rc(deck1, deck2):
    global game
    game += 1
    round = 1
    pdeck = []
    while len(deck1)>0 and len(deck2)>0:
        #print("round", round, "game", locGame, ":", deck1, deck2, deck1[0], deck2[0])
        if (deck1, deck2) in pdeck:
            winner = 1
            #print("round", round, "game", locGame, "winner", winner, "wins by rec stop")
            return winner
        pdeck.append( (deck1[:], deck2[:]) )
        c1 = deck1.pop(0)
        c2 = deck2.pop(0)
        if len(deck1) >= c1 and len(deck2) >= c2:
            ndeck1 = deck1[0:c1]
            ndeck2 = deck2[0:c2]
            winner =  rc(ndeck1, ndeck2)
            #print("round", round, "game", locGame, "winner", winner, "wins by rec")
        else:
            winner = 1 if c1 > c2 else 2
            #print("round", round, "game", locGame, "winner", winner, "wins by card")
        if winner == 1:
            deck1.append(c1)
            deck1.append(c2)
        else: # winner 2
            deck2.append(c2)
            deck2.append(c1)
        round += 1
    return 1 if len(deck1) > 0 else 2

winner = rc(deck1, deck2)

if winner == 1:
    deck = deck1
else:
    deck = deck2

res = 0
for pos, c in zip (reversed(deck), range(1, 999)):
    #print(pos, c)
    res = res + pos * c

print (res)
# 35055
