import sys
import operator
import re
import enum
import re

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines_e='''
1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
'''[1:-1].split('\n')   # split example in lines, keep line endings

m = []

def compute(p, s):
    print (p, s)
    if len(s) == 0:
        return p
    elif s[-1] in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print ("value:", int(s[-1]), s[:-1])
        return compute(int(s[-1]), s[:-1])
    elif s[-1] == '+':
        r = compute(0, s[:-1])
        print (s[-1], p, r)
        return p + r
    elif s[-1] == '-':
        r = compute(0, s[:-1])
        print (s[-1], p, r)
        return p - r
    elif s[-1] == '*':
        r = compute(0, s[:-1])
        print (s[-1], p, r)
        return p * r
    elif s[-1] == '/':
        r = compute(0, s[:-1])
        print (s[-1], p, r)
        return p / r
    elif s[-1] == ')':
        cp = -1
        b = 1
        while b != 0:
            cp = cp - 1
            if s[cp] == '(':
                b = b - 1
            elif s[cp] == ')':
                b = b + 1
        bv = compute (0, s[cp+1:-1] )
        return compute(bv, s[:cp])


total = 0
for line in lines:
    s = line.rstrip('\n')
    s = s.replace(' ', '')
    print ("string:", s)
    i = compute(0, s)
    print ("ergebnis:", s, i)
    print("----------------------------")
    total += i

print ("total", total)
