import sys
import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
'''[1:-1].split('\n')   # split example in lines, keep line endings

rows=len(lines)
seats=[]
for str in lines:
    str = str.rstrip('\n')
    l=[]
    for c in str:
        l.append(c)
    seats.append(l)

columns=len(seats[0])



#seats[2][2] = '#'

print('before')
for row in range(0,rows):
    print(seats[row])
print()

def numocc(row, column):
    numberoccupied = 0
    #print(row, column)
    for diffs in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        (dr, dc) = diffs
        snr = row + dr
        snc = column + dc
        if snr < 0 or snr >= rows or snc < 0 or snc >= columns:
            continue
        while seats[snr][snc] == '.':   # gang
            snrn = snr + dr
            sncn = snc + dc
            if snrn < 0 or snrn >= rows or sncn < 0 or sncn >= columns:
                break
            snr = snrn
            snc = sncn
        #print('sees', snr, snc, seats[snr][snc])
        if seats[snr][snc] == '#':
            numberoccupied += 1
    return numberoccupied

while True:
    makeempty = []
    makeocc = []

    for row in range(0,len(seats)):
        for column in range (0,columns):
            s=seats[row][column]
            if s == '.':    # floor
                continue
            if s == 'L':   ## empty
                #print(row, column, s)
                numberoccupied = numocc(row, column)
                if numberoccupied == 0:
                    makeocc.append( (row, column) )
                #print ('res', row, column, numberoccupied)
                #sys.exit()

            if s == '#':    # occ
                numberoccupied = numocc(row, column)
                if numberoccupied >= 5:
                    makeempty.append( (row, column) )

    #print('here')
    if len(makeempty) + len(makeocc) == 0:
        break
    '''
    print('todos')
    for row in range(0, rows):
        print(seats[row])
    print()
    '''
    for row, column in makeempty:
        seats[row][column] = 'L'
    for row, column in makeocc:
        seats[row][column] = '#'
    '''
    print('after')
    for row in range(0, rows):
        print(seats[row])
    print()
    '''
occ=0
for row in range(0,len(seats)):
        for column in range (0,columns):
            s = seats[row][column]
            if s == '#':
                occ += 1

print(occ)
