import functools
import operator
import collections
from mylib.aoc_frame2 import Day


def parse(text: str):
    """ Compute something from text, as basis for both parts """
    games = []
    for line in text.splitlines():
        lhs, _, rhs = line.partition(": ")
        _, game_str = lhs.split()
        game = int(game_str)
        draws = []
        for draws_str in rhs.split("; "):
            draw = collections.Counter()
            for elements_str in draws_str.split(", "):
                nr_str, color = elements_str.split(" ")
                nr = int(nr_str)
                draw.update({color: nr})
            draws.append(draw)
        games.append((game, draws))
    return games


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        games = parse(text)
        goal = collections.Counter({"red": 12, "green": 13, "blue": 14})
        return sum(game
                   for game, draws in games
                   if all(draw <= goal for draw in draws))

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "configuration"), 8, "example1"


example1 = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        games = parse(text)
        r = 0
        for game, draws in games:
            necessary = collections.Counter()
            for draw in draws:
                necessary = necessary | draw
            r += functools.reduce(operator.mul,
                                  (nr for color, nr in necessary.items()))
        return r

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example2, "configuration"), 2286, "example2"


example2 = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''


Day.do_day(day=2, year=2023, part_a=PartA, part_b=PartB)
