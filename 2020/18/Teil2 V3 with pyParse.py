# Parser für die Grundrechenarten über Integer
# Priority of addop and multop exchanged (made wring!), since AOC task required this exchanged priority

from pyparsing import (
    Literal,
    Word,
    nums,
    Group,
    Forward,
    ParseException,
    Suppress
)
import operator


# stack for parsing nodes, that is build during parsing
exprStack = []
def push_first(toks):
    exprStack.append(toks[0])

# operations for evaluate_stack function
opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv
}

# evaluate node stack that resulted from parting
def evaluate_stack(s):
    op, num_args = s.pop(), 0
    if op in "+-*/^":
        # note: operands are pushed onto the stack in reverse order
        op2 = evaluate_stack(s)
        op1 = evaluate_stack(s)
        return opn[op](op1, op2)
    else:
        return int(op)

# grammar
intNumber = Word(nums)
plus, minus, mult, div = map(Literal, "+-*/")
lpar, rpar = map(Suppress, "()")

addop = plus | minus
multop = mult | div

expr = Forward()
atom = intNumber.setParseAction(push_first) | Group(lpar + expr + rpar)
# attention: for AOC task, priority of addop and multop exchanged by exchanging them in the grammar
term = atom + (addop + atom).setParseAction(push_first)[...]
expr <<= term + (multop + term).setParseAction(push_first)[...]  # <<= sets following exp as body of last forward
grammar = expr


# parse and evaluate an expression
def eval(s):
    exprStack[:] = []
    print(exprStack)
    try:
        results = grammar.parseString(s, parseAll=True)
        val = evaluate_stack(exprStack[:])
    except ParseException as pe:
        print(s, "failed parse:", str(pe))
    except Exception as e:
        print(s, "failed eval:", str(e), exprStack)
    return val


# -------------------------------------------------------------------------------

with open('input.txt') as f:
    lines = f.readlines()  # # read complete file, results in list of lines with endings

# For using test input instead of file input rename from lines_example to lines
linesex='''
1 + 2 * 3 + 4 * 5 + 6
1 + (2 * 3) + (4 * (5 + 6))
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2
'''[1:-1].split('\n')   # split example in lines, keep line endings


total = 0
for line in lines:
    s = line.rstrip('\n')
    s = s.replace(' ', '')
    print ("string:", s)
    i = eval(s)
    print ("ergebnis:", s, i)
    print("----------------------------")
    total += i

print ("total", total)
# 340789638435483