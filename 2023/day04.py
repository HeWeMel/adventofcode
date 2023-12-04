from collections import defaultdict
from mylib.aoc_frame2 import Day


def parse(text: str):
    """ Compute something from text, as basis for both parts """
    for card_str in text.splitlines():
        card_title, numbers = card_str.split(": ")
        _, card_id_str = card_title.split()
        card_id = int(card_id_str)
        winning_str, my_str = numbers.split(" | ")
        winning_numbers = set(int(s) for s in winning_str.split())
        my_numbers = set(int(s) for s in my_str.split())
        yield card_id, winning_numbers & my_numbers


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        result = 0
        for card_id, my_winning_numbers in parse(text):
            win = 0
            for n in my_winning_numbers:
                win = 2 * win if win > 0 else 1
            result += win
        return result

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 13, "example1"


example1 = '''
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
'''


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        card_multiple = defaultdict(int)  # for each card id: how many do we have?
        for card_id, my_winning_numbers in reversed(list(parse(text))):
            cards = 1
            matches = 0
            for n in my_winning_numbers:
                matches += 1
                cards += card_multiple[card_id + matches]
            card_multiple[card_id] = cards
        return sum(i for i in card_multiple.values())

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 30, "example1"


Day.do_day(day=4, year=2023, part_a=PartA, part_b=PartB)
