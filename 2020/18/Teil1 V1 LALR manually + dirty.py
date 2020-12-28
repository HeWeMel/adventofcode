import sys
import operator
import re
import enum
import re

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines_e = '''
1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
'''[1:-1].split('\n')  # split example in lines, keep line endings

intAsChars = list(map(str, range(10)))
charOpToOp = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv, }

def compute(p, s):  # p = previous = value of already evaluated expression part on the right, s = string to evaluate
    print(p, s)
    if len(s) == 0:
        return p
    c, r = s[-1], s[:-1]
    if c in intAsChars:
        print("value:", int(c), r)
        return compute(int(c), r)
    elif c in charOpToOp:
        r = compute(0, r)
        print(c, p, r)
        return (charOpToOp[c])(p, r)
    elif c == ')':
        cp = 0  # character position from the right
        b = 1 # one bracket level open
        while b != 0:
            cp = cp - 1
            if r[cp] == '(':
                b = b - 1
            elif r[cp] == ')':
                b = b + 1
        bv = compute(0, r[cp + 1:])  # right after opening bracket till end (closing bracket already removed)
        return compute(bv, r[:cp])  # string up to (exclusive) opening bracket


total = 0
for line in lines:
    s = line.rstrip('\n')
    s = s.replace(' ', '')
    print("string:", s)
    i = compute(0, s)
    print("ergebnis:", s, i)
    print("----------------------------")
    total += i

print("total", total)
# 67800526776934
