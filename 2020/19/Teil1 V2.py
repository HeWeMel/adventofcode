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
    allmessages = set()
    for opt in opts:  # for all options of the rule (examples: 1 2 3 or 1 2 | 3 4):
        allmessages = allmessages.union(
            functools.reduce(
                (lambda mgs1, mgs2: # combine possible message beginnings with possible following parts
                 [m1 + m2 for m1, m2 in itertools.product( mgs1, mgs2)]
                ), (messages[r] for r in opt))  # for the messages of all sub rules of the option
        )
    messages[i] = allmessages  # store messages of the rule, without duplications
do(0)
ok = messages[0]
print("messages computed", len(ok))

# ------------- count correct input messages --------------
n = len( set(ok).intersection( input_str.split("\n") ))     # messages, that are ok and input
print(n, "messages valid")
#285