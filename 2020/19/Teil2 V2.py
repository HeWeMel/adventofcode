import re
import itertools
import functools

with open('input.txt') as f:
    lines = f.read()  # read complete file, results string of lines with endings

rules_str, input_str = lines.split('\n\n')  # two blocks, one with rules, one with messages


# ------------- rules --------------
messages = dict()  # messages that can be generated
dep = dict()  # dependencies for the message calculation: rule depends on which rules?
rules = dict()  # all rules
for s in rules_str.split("\n"):
    s = s.rstrip('\n')
    i, r = s.split(": ")
    i = int(i)
    if r[0] == '"':  # terminal rule:
        rt = r.strip('"')
        rules[i] = ["terminal", rt]  # put rule to rule list
        messages[i] = (rt,)  # put string to possible message
    else:  # non terminal rule:
        opts_s = r.split(" | ")
        deps = set()
        opts = []
        for o in opts_s:  # for all options of the rule:
            nn = o.split(" ")
            nn = [int(i) for i in nn]
            opts.append(nn)  # collect sequence of sub rules of the option
            deps = deps.union(nn)  # collect set of sub rules of all options of the rule
        rules[i] = ["contains", opts]  # take rule to rule list
        dep[i] = deps  # take dependencies of the rule to the dependencies


# ------------- rules to possible messages --------------
visited = set()
def do(i):
    if i in visited:  # depth first search
        return
    visited.add(i)
    if i not in dep:    # terminal: done
        return
    for j in dep[i]:    # non terminal: recurse
        do(j)
    (t, opts) = rules[i]  # when leaving a non terminal rule (that gives a topological sorting):
    #print("rule", i, t, opts)
    allmessages = set()
    for opt in opts:  # for all options of the rule (examples: 1 2 3 or 1 2 | 3 4):
        allmessages = allmessages.union(
            functools.reduce(
                (lambda mgs1, mgs2: # combine possible message beginnings with possible following parts
                 [m1 + m2 for m1, m2 in itertools.product( mgs1, mgs2)]
                ), (messages[r] for r in opt))  # for the messages of all sub rules of the option
        )
    messages[i] = list(allmessages)  # store messages of the rule, without duplications

do(42)  # start message calculations for rule 42 and 31
do(31)

m42 = messages[42]  # messages of the new starting nodes
m31 = messages[31]
for m in m42 + m31: # check, that all messages have length 8
    if len(m) != 8:
        raise RuntimeError
if len( set(m42).intersection(m31)) != 0:  # check, that sets of messages are disjoint
    raise RuntimeError


# ------------- read messages --------------
msg = []
for s in input_str.split("\n"):
    s = s.rstrip('\n')
    msg.append(s)


# New extra rules, will be implemented manually
# 8: 42 | 42 8               = 42+
# 11: 42 31 | 42 11 31       = 42*n 31*n, n>0
# 0: 8 11                    = 42+ (n*42 n*31), n>0

def check_code(code):
    # check code string for pattern: y+(n*y)(n*x) with n>0
    mo = re.fullmatch(r'(y+)(x+)', code)
    if mo == None:
        return False
    ys, xs = mo.groups()
    return len(ys) > len(xs)


res = 0 # count of matching input messages
for s in msg:
    l = len(s)
    if l % 8 != 0:  # since all messages of rules 31 and 42 have length 8,
        continue    # length of messages of rule 0 must be a multiple of 8

    ok = True
    code = ""
    for i in range(0, l, 8):    # walk through 8 character substrings of message
        sp = s[i:i + 8]
        if sp in m31:           # if substring is a message of rule 31, note an "x"
            code = code + "x"
        elif sp in m42:         # if substring is a message of rule 42, note an "y"
            code = code + "y"
        else:                   # other sub strings make message directly illegal
            ok = False
            break
    if not ok:
        continue

    if check_code(code):        # check code for character pattern "y+(n*y)(n*x) with n>0"
        res += 1
print(res)
# 412