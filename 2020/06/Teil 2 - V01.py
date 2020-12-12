import sys
import functools

with open('input.txt', 'r') as f:
    lines= (f.readlines())
lines = [ line[:-1] for line in lines ]
lines.append('')

#print(len(lines))

groups=[]
group=[]
for line in lines:
    #print (line)
    if len(line)!=0:
        group.append(set(line))
    else:
        groups.append(group)
        group=[]

sum_group_answers=0
for group in groups:
    for line in group:
        print(line)
    answers=functools.reduce( lambda a, b: a.intersection(b), group )
    print(answers)
    print('---')
    sum_group_answers += len(answers)

print(sum_group_answers)
sys.exit()
