import itertools
import functools
from mylib.aoc_frame import Day


def tokenize(fish):  # from fish string to mutable list of fish tokens, with integers evaluated
    return [e if e in ("[", "]", ",") else int(e) for e in fish]


def reduce_once(fish):  # do one step of reduction, if one of the two rules can be applied
    # find a pair to explode
    depth = 0
    for i in range(len(fish)):
        if fish[i] == "[":
            depth += 1
            if depth > 4 and fish[i+1] != "[" and fish[i+3] != "[":
                l_val, r_val = fish[i+1], fish[i+3]  # pair of num, and too deep: explode

                for j in range(i, 0, -1):  # from left of my opening bracket till begin
                    if fish[j] not in ("[", "]", ","):  # num found: add left value there
                        fish[j] = fish[j] + l_val
                        break

                for j in range(i+5, len(fish)):  # from right of my closing bracket till end
                    if fish[j] not in ("[", "]", ","):  # num found: add right value there
                        fish[j] = fish[j] + r_val
                        break

                return fish[:i] + [0, ] + fish[i+5:]  # replace pair with brackets by 0
        elif fish[i] == "]":
            depth -= 1
    # if there is no pair to explode, find first split case
    for i in range(len(fish)):
        if fish[i] not in ("[", "]", ","):  # int
            v = fish[i]
            if v > 9:
                return fish[:i] + ["[", v//2, ",", (v+1)//2, "]"] + fish[i+1:]
    # no rule matches: return fish unchanged
    return fish


def reduce(fish):  # reduce fish till fix point
    fn = reduce_once(fish)
    return fish if fn == fish else reduce(fn)


def add_two_fish(f1, f2):  # build a pair of the two fish, and reduce result
    return reduce(["[", ] + f1 + [",", ] + f2 + ["]", ])


def add_all_fish(fish_str):  # from text of fish specification to sum of all fish
    return functools.reduce(add_two_fish, (reduce(tokenize(f)) for f in fish_str.splitlines()))


def eval_fish(fish):  # Recursively evaluate nested data in fish tokens to: (result, unused tokens)
    if fish[0] == "[":
        result1, rest1 = eval_fish(fish[1:])   # eval chars after the opening bracket
        result2, rest2 = eval_fish(rest1[1:])  # eval chars after the comma
        return 3*result1 + 2*result2, rest2[1:]  # rest is everything after the closing bracket
    else:
        return fish[0], fish[1:]  # evaluate number


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return eval_fish(add_all_fish(d.text))[0]


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        some_fish = (reduce(tokenize(f)) for f in d.text.splitlines())
        return max(eval_fish(add_two_fish(f1, f2))[0]
                   for f1, f2 in itertools.permutations(some_fish, 2))


Day.do_day(day=18, year=2021, part_a=PartA, part_b=PartB)
