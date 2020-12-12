import re, sys

with open('input.txt') as f:
    pw_ok=0
    for line in f:
        #3-4 n: nnnmn
        (low, high, c, nothing, pw, nothing) = re.split(r'[- :\n]', line)
        n=pw.count(c)
        print(low, high, c, pw, n)
        if int(low)<=n and n<=int(high):
            pw_ok+=1
    print (pw_ok)
# 645
