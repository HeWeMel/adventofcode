import sys
import re

with open('input.txt', 'rt') as f:
    lines = f.readlines()  # ganze Datei lesen

pat_rule = re.compile(r"(.+) bags contain (.+)[.]")
pat_split = re.compile(r", |[.]")
pat_tobags = re.compile(r"(\d+) (.+)+ bag(?:s?)")

rules = dict()
outer = dict()
for line in lines:
    # print(":", line[:-1])
    m = pat_rule.match(line)
    (f, to_text) = m.groups()
    t = []
    if to_text != 'no other bags':
        tos = pat_split.split(to_text)
        if len(tos) == 0:
            print('no tos in line:', line)
            sys.exit()
        for bag in tos:
            m = pat_tobags.match(bag)
            (n, b) = m.groups()
            if int(n) == 0:
                print('empty to')
                sys.exit()  # normal hier: break
            t.append((n, b))
            if not (b in outer):
                outer[b] = []
            outer[b].append(f)
    # print (f">> '{f}' -> {t}")
    # print()
    if f in rules:
        print('Outer bag tritt zweites Mal auf:', line)
        sys.exit()
    rules[f] = t
print(len(rules), 'rules')

# for key in outer:
#    print(key, outer[key])
# print(outer)
# sys.exit()

done = []
todos = ['shiny gold']
r = []
round = 1
while len(todos) != 0:
    # print(todos)
    new_todos = []
    for o in todos:
        if o in done: continue
        print(o)
        done.append(o)
        if round == 1:
            round += 1
        else:
            r.append(o)
        if o in outer:
            new_todos.extend(outer[o])
    todos = new_todos

print(r)
print(len(r))
