import re, sys

with open('input.txt') as f:

    pw_ok=0
    for line in f:
        (rule,s,space_and_pw) = line.partition(':')
        (lowhigh,s,c) = rule.partition(' ')
        (low,s,high) = lowhigh.partition('-')
        pw=space_and_pw[1:-1]
        n=pw.count(c)
        print(low, high, c, pw, n)
        if int(low)<=n and n<=int(high):
            pw_ok+=1
    print (pw_ok)
# 645
