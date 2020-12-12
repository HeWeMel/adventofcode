import re

with open('input.txt', 'r') as f:

    pw_ok=0
    for line in f:
        (rule,s,space_and_pw) = line.partition(':')
        (lowhigh,s,c) = rule.partition(' ')
        (low,s,high) = lowhigh.partition('-')
        pw=space_and_pw[1:-1]
        c1=pw[int(low)-1]
        c2=pw[int(high)-1]
        if (c1==c and c2!=c) or (c1!=c and c2==c):
            print(low, high, c, pw, c1, c2, 'ok')
            pw_ok+=1
        else:
            print(low, high, c, pw, c1, c2, 'falsch')
    print (pw_ok)
#737