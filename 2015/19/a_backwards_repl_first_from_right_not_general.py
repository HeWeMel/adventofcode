import itertools
import re
from collections import defaultdict
from aocd.models import Puzzle
from mylib.aoc_frame import Day
from collections.abc import Iterator
from typing import Iterable
import functools


class PartA(Day):

    @staticmethod
    def replace_two_character_pairs(text: str) -> str:
        """
        Replace two-character strings like [A-Z][a-z] by a (new) single character,
        a number. Works only up to 10 distinct two-character strings.
        """
        distinct_pairs = set(re.findall(r"[A-Z][a-z]", text))
        i = 0
        for pair in distinct_pairs:
            if i > 9:
                raise RuntimeError("More than 10 two-character tokens")
            text = text.replace(pair, str(i))
            i += 1
        return text

    @staticmethod
    def text_to_medicine_and_rules(text: str) -> tuple[str, dict[str, list[str]]]:
        """
        Parse text into the medicine string and the rules. Report the rules as
        dictionary from the left-side string to a list of right-side strings.
        """
        lines = text.splitlines()

        medicine = lines[-1]

        rules = defaultdict(list)
        right_strings = set()
        for line in lines[0:-2]:
            left, right = line.split(" => ")
            rules[left].append(right)
            right_strings.add(right)

        return medicine, rules

    def parse(self, text, d):
        """ Simplify the input, parse it, and store medicine and rules in *d* """
        text = self.replace_two_character_pairs(text)
        d.medicine, d.rules = self.text_to_medicine_and_rules(text)

    @staticmethod
    def apply_rules_at_position(
            s: str, i: int, rules: dict[str, list[str]]
    ) -> Iterator[str]:
        """
        Apply each matching rule on the one-character string s[i] and yiels the
        results
        """
        c_from = s[i]
        for to_c in rules[c_from]:
            medicine_variant_list = list(s)
            medicine_variant_list[i] = to_c
            medicine_variant = "".join(medicine_variant_list)
            yield medicine_variant

    def compute(self, d):
        """
        For each character in the medicine string, apply all matching rules.
        Collect the results and return their number.
        """
        variants = set()
        for i in range(len(d.medicine)):
            variants.update(self.apply_rules_at_position(d.medicine, i, d.rules))
        return len(variants)

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, None), 4, "example1"
        yield self.test_solve(example2, None), 7, "example2"
        yield self.test_solve(example3, None), 7, "example3"


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

example3 = '''
Ho => HoO
Ho => OHo
O => HoHo

HoOHoOHoO
'''


class PartB(PartA):

    def compute(self, d):
        """
        """
        medicine = d.medicine

        rules_backwards = defaultdict(list)
        for from_string, to_strings in d.rules.items():
            for to_string in to_strings:
                rules_backwards[to_string].append(from_string)

        def apply_first_matching_rule(s: str) -> str:
            for i in range(len(molecule)-1, -1, -1):
                for from_string, to_strings in rules_backwards.items():
                    if molecule[i:i+len(from_string)] == from_string:
                        for to_string in to_strings:
                            new_molecule_lst = list(molecule)
                            new_molecule_lst[i:i+len(from_string)] = to_string
                            new_molecule = "".join(new_molecule_lst)
                            if to_string == "e" and new_molecule != "e":
                                continue
                            return new_molecule
            raise RuntimeError()

        molecule = medicine
        for depth in itertools.count():
            if molecule == "e":
                return depth
            molecule = apply_first_matching_rule(molecule)
            print(molecule)
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
