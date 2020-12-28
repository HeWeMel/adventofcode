import sys
import operator
import re
import enum
import re
import collections

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

# LALR(0) grammar:
# value_or_brackets = ( expression ) | [0..9]
# expression = expression [+-*/] value_or_brackets | value_or_brackets

intAsChars = list(map(str, range(10)))
charOpToOp = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv, }

def evaluate_value_or_brackets(tokens):
    # print("> value or brackets", s)
    if len(tokens) == 0:
        raise RuntimeError("cannot evaluate empty string")
    c = tokens.pop()
    if c in intAsChars:
        v = int(c)
        # print("< value:", int(c))
        return v
    elif c == ')':
        v = evaluate_expression(tokens)
        c = tokens.pop()
        if c != '(':
            raise RuntimeError("opening bracket expected, but found:", c, "after string", tokens)
        # print("< brackets", r, ":", v)
        return v
    else:
        raise RuntimeError("number or brackets expected, but found:", c, "after string", tokens)

def evaluate_expression(tokens):
    # print("> expression", s)
    if len(tokens) == 0:
        raise RuntimeError("cannot evaluate empty string")
    v = evaluate_value_or_brackets(tokens)
    if len(tokens) == 0 or tokens[-1] not in charOpToOp:
        return v  # no next character that does match
    op = tokens.pop()
    left_v = evaluate_expression(tokens)
    r = (charOpToOp[op])(left_v, v)
    # print("< expression", s, ":", left_v, op, v)
    return r

def evaluate(s):
    tokens = collections.deque(s)
    v = evaluate_expression(tokens)
    if len(tokens) != 0:
        raise RuntimeError("unmatched tokens:", tokens)
    return v

total = 0
for line in lines:
    s = line.rstrip('\n')
    s = s.replace(' ', '')
    print("string:", s)
    i = evaluate(s)
    print("result for", s, ":", i)
    print("----------------------------")
    total += i

print("total", total)
# 67800526776934
