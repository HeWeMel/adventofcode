
with open('input.txt') as f:
    t=f.read()              # read complete file, results string of lines with endings

# For using test input instead of file input rename from lines_example to lines
tex='''
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


part1, part2 = t.split('\n\n')

deck1 = []
deck2 = []
for line in part1.split('\n')[1:]:
    line = line.rstrip('\n')  # lines in block
    deck1.append(int(line))
for line in part2.split('\n')[1:]:
    line = line.rstrip('\n')  # lines in block
    deck2.append(int(line))

while len(deck1)>0 and len(deck2)>0:
    c1 = deck1.pop(0)
    c2 = deck2.pop(0)
    if c1 > c2:
        deck1.append(c1)
        deck1.append(c2)
    else: # c2 > c1
        deck2.append(c2)
        deck2.append(c1)

if len(deck1) == 0:
    deck = deck2
else:
    deck = deck1

res = 0
for pos, c in zip (reversed(deck), range(1, 999)):
    res = res + pos * c

print (res)
# 33098