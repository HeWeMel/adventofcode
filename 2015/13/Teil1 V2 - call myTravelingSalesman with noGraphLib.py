import sys
import re
import itertools
import functools
import collections
import timeit
from myTravelingSalesman import traveling_salesman, Path


def parse(puzzle_id, puzzle: list[str]):
    happiness = collections.defaultdict(lambda: collections.defaultdict(int))

    for s in puzzle:
        s = s.rstrip()
        person1, _would, verb, units_raw, _happiness, _units, _by, _sitting, _next, _to, person2_raw = s.split(' ')
        units = int(units_raw)
        person2 = person2_raw.rstrip('.')

        if verb == 'lose':
            units = -units

        # mutual happiness gain added, gives weight for edges in both directions
        happiness[person1][person2] += units
        happiness[person2][person1] += units
    return happiness


def solve(puzzle_id, happiness):
    print("here")
    length, path = traveling_salesman(happiness, find_longest=True)
    if length is None:  # not found
        return None
    print("found longest path for problem:", length)
    print([path._traverse()])
    print()
    return length


def parse_and_solve(puzzle_id, puzzle):
    result = ''
    start = timeit.default_timer()

    result = solve(puzzle_id, parse(puzzle_id, puzzle))

    stop = timeit.default_timer()
    print('Time: ', stop - start)
    print("result for puzzle", puzzle_id, ":", result)

    return result


def solve_and_check(puzzle_id, puzzle, correct_result):
    result = parse_and_solve(puzzle_id, puzzle)
    if result != correct_result:
        print("puzzle", puzzle_id, ": result", result,
              "instead of correct", correct_result)
        raise RuntimeError("wrong result")
    print("------------------------------------------")


puzzle = '''
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''[1:-1].split('\n')   # split example in lines, keep line endings
solve_and_check(1, puzzle, 330)

with open('input.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    solve_and_check('real input', puzzle, 664)

with open('input2.txt') as f:
    puzzle = f.readlines()  # read complete file, results in list of lines with endings
    # print(parse_and_solve('real input 2', puzzle))
    solve_and_check('real input 2', puzzle, 640)
