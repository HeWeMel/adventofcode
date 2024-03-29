# -- Computation of results for different step counts
steps = 131*4+65  # Result: 313365
tiles = (steps - 65) // 131

r = 0
# inner
for y in range(-(tiles-1), (tiles-1)+1):
    for x in range(1+2*((tiles-1)-abs(y))):
        v = 7734 if x % 2 == 0 else 7719
        print(y, v)
        r += v

# boundary
r += 986 + 5812 + 962
print("986 + 5812 + 962")
for y in range(-(tiles-1), (tiles-1)+1):
    if y < 0:
        print("986 + 6768 + 6763 + 962")
        r += 986 + 6768 + 6763 + 962
    elif y == 0:
        print("5828 + 5808")
        r += 5828 + 5808
    else:
        print("992 + 6779 + 6764 + 974")
        r += 992 + 6779 + 6764 + 974

print("992 + 5824 + 974")
r += 992 + 5824 + 974

print()
print(r)
print()

# -- Fast computation of results for different step counts

steps = 26501365  # Result: 632421652138917
# steps = 131*4+65  # Result: 313365

tiles = (steps - 65) // 131  # 202.300 for 26501365

r = 0
# inner
incr = 7734
for y in range(-(tiles-1), 0):
    r += 2 * incr
    incr += 7719 + 7734
r += incr

# boundary
r += 986 + 5812 + 962
for y in range(-(tiles-1), (tiles-1)+1):
    if y < 0:
        r += 986 + 6768 + 6763 + 962
    elif y == 0:
        r += 5828 + 5808
    else:
        r += 992 + 6779 + 6764 + 974
r += 992 + 5824 + 974

print(r)


# -- Data from day21_optimized.py for chosen states
# (state from loops of tiles, then boundary tile states)

""" Data for 131*4+65
(-3, 0) 7734
(-2, -1) 7734
(-2, 0) 7719
(-2, 1) 7734
(-1, -2) 7734
(-1, -1) 7719
(-1, 0) 7734
(-1, 1) 7719
(-1, 2) 7734
(0, -3) 7734
(0, -2) 7719
(0, -1) 7734
(0, 0) 7719
(0, 1) 7734
(0, 2) 7719
(0, 3) 7734
(1, -2) 7734
(1, -1) 7719
(1, 0) 7734
(1, 1) 7719
(1, 2) 7734
(2, -1) 7734
(2, 0) 7719
(2, 1) 7734
(3, 0) 7734

(-4, -1) 986
(-4, 0) 5812
(-4, 1) 962
(-3, -2) 986
(-3, -1) 6768
(-3, 1) 6763
(-3, 2) 962
(-2, -3) 986
(-2, -2) 6768
(-2, 2) 6763
(-2, 3) 962
(-1, -4) 986
(-1, -3) 6768
(-1, 3) 6763
(-1, 4) 962
(0, -4) 5828
(0, 4) 5808
(1, -4) 992
(1, -3) 6779
(1, 3) 6764
(1, 4) 974
(2, -3) 992
(2, -2) 6779
(2, 2) 6764
(2, 3) 974
(3, -2) 992
(3, -1) 6779
(3, 1) 6764
(3, 2) 974
(4, -1) 992
(4, 0) 5824
(4, 1) 974

313365
"""

""" Data for 131*5+65
(-4, 0) 7734
(-3, -1) 7734
(-3, 0) 7719
(-3, 1) 7734
(-2, -2) 7734
(-2, -1) 7719
(-2, 0) 7734
(-2, 1) 7719
(-2, 2) 7734
(-1, -3) 7734
(-1, -2) 7719
(-1, -1) 7734
(-1, 0) 7719
(-1, 1) 7734
(-1, 2) 7719
(-1, 3) 7734
(0, -4) 7734
(0, -3) 7719
(0, -2) 7734
(0, -1) 7719
(0, 0) 7734
(0, 1) 7719
(0, 2) 7734
(0, 3) 7719
(0, 4) 7734
(1, -3) 7734
(1, -2) 7719
(1, -1) 7734
(1, 0) 7719
(1, 1) 7734
(1, 2) 7719
(1, 3) 7734
(2, -2) 7734
(2, -1) 7719
(2, 0) 7734
(2, 1) 7719
(2, 2) 7734
(3, -1) 7734
(3, 0) 7719
(3, 1) 7734
(4, 0) 7734

(-5, -1) 986
(-5, 0) 5812
(-5, 1) 962
(-4, -2) 986
(-4, -1) 6768
(-4, 1) 6763
(-4, 2) 962
(-3, -3) 986
(-3, -2) 6768
(-3, 2) 6763
(-3, 3) 962
(-2, -4) 986
(-2, -3) 6768
(-2, 3) 6763
(-2, 4) 962
(-1, -5) 986
(-1, -4) 6768
(-1, 4) 6763
(-1, 5) 962
(0, -5) 5828
(0, 5) 5808
(1, -5) 992
(1, -4) 6779
(1, 4) 6764
(1, 5) 974
(2, -4) 992
(2, -3) 6779
(2, 3) 6764
(2, 4) 974
(3, -3) 992
(3, -2) 6779
(3, 2) 6764
(3, 3) 974
(4, -2) 992
(4, -1) 6779
(4, 1) 6764
(4, 2) 974
(5, -1) 992
(5, 0) 5824
(5, 1) 974

467992
"""