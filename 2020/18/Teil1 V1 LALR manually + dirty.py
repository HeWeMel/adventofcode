import sys
import operator
import re
import enum
import re

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
lines_example = '''
1 + 2 * 3 + 4 * 5 + 6
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
'''[1:-1].split('\n')  # split example in lines, keep line endings

intAsChars = list(map(str, range(10)))
charOpToOp = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.floordiv, }


def compute(res_right, expr):  # intermediate result, remaining expression to evaluate --> result, new remaining expr
    # print(p, s)
    if len(expr) == 0:
        return res_right, expr  # nothing to evaluate any more: intermediate result is final result, empty todos
    c, r = expr[-1], expr[:-1]
    if c in intAsChars:
        if res_right != None:
            raise RuntimeError("int", int(c), "at unexpected place, partial result", res_right, "remaining expr", r)
        # print("value:", int(c), r)
        return compute(int(c), r)  # int: evaluate expression to the left with current value as intermediate result
    elif c in charOpToOp:
        res_left, rest_new = compute(None, r)  # op: new evaluation (intermediate result 0) to the left and ...
        # print("after recursion apply operation, left result, prev result:", c, res, p)
        return (charOpToOp[c])(res_left, res_right), rest_new  # ... apply op to result with intermediate result
    elif c == ')':  # opening (from the right) brackets:
        res_bracket, rest_new = compute(None, r)  # new evaluation (intermediate result 0) of the content of brackets
        return compute(res_bracket, rest_new)  # use as new intermediate result for evaluation left of the brackets
    elif c == '(':  # closing (from the right) brackets: return from sub evaluation.
        return res_right, r  # intermediate result is result, and new remaining expression is expr left of brackets
    else:
        raise RuntimeError("unexpected token", c, "with remaining expression", r)

total = 0
for line in lines:
    s = line.rstrip('\n')
    s = s.replace(' ', '')
    # print("string:", s)
    i, r = compute(None, s)
    if r!= "":
        raise RuntimeError("input could not be parsed completely, rest:", r)
    print("result:", s, i)
    # print("----------------------------")
    total += i

print("total", total)
# 67800526776934
