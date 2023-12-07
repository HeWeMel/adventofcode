import collections
from mylib.aoc_frame2 import Day


def parse(text: str, joker=""):
    """ Compute something from text, as basis for both parts """
    card_strengths = {card: strength
                      for strength, card in enumerate(reversed("AKQJT98765432"))
                      if card != joker}
    card_strengths[joker] = -1

    hands = []
    for hand_str in text.splitlines():
        hand, bid_str = hand_str.split()
        bid = int(bid_str)

        nr_of_j = sum(1 for card in hand if card == joker)

        counts = list(sorted([count for card, count in collections.Counter(hand).items()
                              if card != joker],
                             reverse=True))
        if len(counts) == 0:
            # Special case: 5 jokers
            counts = [5]
        else:
            # Add count of joker to count of card with maximal count
            counts[0] += nr_of_j
        counts = tuple(counts)
        card_strength = tuple(card_strengths[card] for card in hand)
        hands.append((counts, card_strength, hand, bid))
    return hands


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        return sum(rank * hand[-1]
                   for rank, hand in enumerate(sorted(parse(text)), 1))

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 6440, "example1"


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        return sum(rank * hand[-1]
                   for rank, hand in enumerate(sorted(parse(text, "J")), 1))

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 5905, "example2"


example1 = '''
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''


Day.do_day(day=7, year=2023, part_a=PartA, part_b=PartB)
