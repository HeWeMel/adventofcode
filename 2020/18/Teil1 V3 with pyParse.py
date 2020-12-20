# Parser für die Grundrechenarten über Integer
# In line 31ff and 44ff, addop and multop defined as equally strong ops, as required in AOC task

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

exprStack = []


def push_first(toks):
    exprStack.append(toks[0])


bnf = None


def BNF():
    """
    op  :: '*' | '/' | '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: integer | '(' expr ')'
    expr    :: atom [ op atom ]*
    """
    global bnf
    if not bnf:
        intNumber = Word(nums)
        plus, minus, mult, div = map(Literal, "+-*/")
        lpar, rpar = map(Suppress, "()")
        op = plus | minus | mult | div

        expr = Forward()
        atom = intNumber.setParseAction(push_first) | Group(lpar + expr + rpar)
        expr <<= atom + (op + atom).setParseAction(push_first)[...]  # <<= sets following exp as body of last forward
        bnf = expr
    return bnf


opn = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv
}


def evaluate_stack(s):
    op, num_args = s.pop(), 0
    if op in "+-*/^":
        # note: operands are pushed onto the stack in reverse order
        op2 = evaluate_stack(s)
        op1 = evaluate_stack(s)
        return opn[op](op1, op2)
    else:
        return int(op)


def eval(s):
    exprStack[:] = []
    try:
        results = BNF().parseString(s, parseAll=True)
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
# 67800526776934