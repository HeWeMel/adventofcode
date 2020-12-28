import operator
import collections

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines_example = '''
1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
'''[1:-1].split('\n')  # split example in lines, keep line endings

# LALR(1) grammar:
# value_or_brackets = ( expression ) | [0..9]
# strong_expression = strong_expression [+-] value_or_brackets | value_or_brackets
# expression = expression [*/] strong_expression | strong_expression

intAsChars = list(map(str, range(10)))
charOpToOp = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv, }
strongOpChars = set( ['+', '-'] )

def evaluate_value_or_brackets(tokens):
    # print("> value or brackets", tokens)
    if len(tokens) == 0:
        raise RuntimeError("cannot evaluate empty string")
    c = tokens.pop()
    if c in intAsChars:
        v = int(c)
        # print("< value:", int(c), "rest", tokens)
        return v
    elif c == ')':
        v = evaluate_expression(tokens)
        c = tokens.pop()
        if c != '(':
            raise RuntimeError("opening bracket expected, but found:", c, "after string", tokens)
        # print("< brackets", tokens, ":", v)
        return v
    else:
        raise RuntimeError("number or brackets expected, but found:", c, "after string", tokens)

def evaluate_strong_expression(tokens):
    # print("> strong expression", tokens)
    if len(tokens) == 0:
        raise RuntimeError("cannot evaluate empty string")
    v = evaluate_value_or_brackets(tokens)
    if len(tokens) == 0 or tokens[-1] not in strongOpChars:
        # print("< expression result because expression is finished, rest:", tokens)
        return v  # no next character that does match
    op = tokens.pop()
    # print("op:", op)
    left_v = evaluate_strong_expression(tokens)
    r = (charOpToOp[op])(left_v, v)
    # print("< strong expression", s, ":", left_v, op, v)
    return r


def evaluate_expression(tokens):
    # print("> expression", tokens)
    if len(tokens) == 0:
        raise RuntimeError("cannot evaluate empty string")
    v = evaluate_strong_expression(tokens)
    if len(tokens) == 0 or tokens[-1] not in charOpToOp:
        # print("< expression result because expression is finished, rest:", tokens)
        return v  # no next character that does match
    op = tokens.pop()
    # print("op:", op)
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
    # print("string:", s)
    i = evaluate(s)
    print("result for", s, ":", i)
    # print("----------------------------")
    total += i

print("total", total)
# 340789638435483
