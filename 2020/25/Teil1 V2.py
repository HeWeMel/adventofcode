# puzzle data
card_pk = 8421034
door_pk = 15993936

# example data
if False:
    card_pk = 5764801
    door_pk = 17807724

def transform (subject, loopsize):
    v = 1
    for i in range(loopsize):
        v = v * subject
        v = v % 20201227
    return v

loopsize = 1
lc = 0
ld = 0
v = 1
while lc == 0 or ld == 0:
    v = v * 7
    v = v % 20201227
    if v == card_pk:
        lc = loopsize
    if v == door_pk:
        ld = loopsize
    loopsize += 1

print(ld, lc)
key = transform(door_pk, lc)
print(key)
# 9177528