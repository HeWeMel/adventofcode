from collections import defaultdict
from mylib.aoc_frame import Day
import re
import nographs as nog


class PartA(Day):
    def parse(self, text, d):
        """ Store puzzle parsing result data into attributes of d """
        lines = text.splitlines()
        # Last line is medicine string
        d.medicine = lines[-1]
        # Rules as mapping from left side to list of right sides
        d.rules = defaultdict(list)
        for line in lines[0:-2]:
            left, right = line.split(" => ")
            d.rules[left].append(right)

    @staticmethod
    def generate(s, rules):
        """ Generate all variants of s resulting from applying one of the rules """
        for from_string, to_strings in rules.items():
            for match in re.finditer(from_string, s):
                start, end = match.span()
                for replacement in to_strings:
                    yield s[0:start] + replacement + s[end:]

    def compute(self, d):
        """ Return puzzle result, get parsing data from attributes of d """
        # Generate one-step variants of medicine and count distinct variants
        return len(set(self.generate(d.medicine, d.rules)))

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, None), 4, "example1"
        yield self.test_solve(example2, None), 7, "example2"


example1 = '''
H => HO
H => OH
O => HH

HOH
'''

example2 = '''
H => HO
H => OH
O => HH

HOHOHO
'''


class PartB(PartA):
    def compute(self, d):
        """ Store puzzle parsing result data into attributes of d """
        # Reverse the rules
        rules_backwards = defaultdict(list)
        for from_string, to_strings in d.rules.items():
            for to_string in to_strings:
                rules_backwards[to_string].append(from_string)

        def next_edges(s, _):
            """ Edges in our graph go from a given string to all variants
            resulting from the application of one of the rules in backwards
            direction. Such a step costs 1 cost unit. """
            for variant in self.generate(s, rules_backwards):
                yield variant, 1

        def heuristic(s):
            """ The estimation for the costs to the goal is the number
            of characters we still have to reduce to come to the
            one-character goal string. """
            return len(s) - 1

        # We use the A-star traversal strategy to find the weight-shortest path from the
        # medicine back to the "e"-string. Since the weight of each edge is one, we
        # find the shortest paths in the number of edges (number of rules applied).
        t = nog.TraversalAStar(next_edges)
        for m in t.start_from(heuristic, d.medicine):
            if m == "e":
                return t.depth
        return None

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example4, None), 3, "example4"
        yield self.test_solve(example5, None), 6, "example5"


example4 = '''
e => H
e => O
H => HO
H => OH
O => HH

HOH
'''

example5 = '''
e => H
e => O
H => HO
H => OH
O => HH

HOHOHO
'''

Day.do_day(day=19, year=2015, part_a=PartA, part_b=PartB)
