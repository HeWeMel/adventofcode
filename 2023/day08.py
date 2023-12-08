import itertools
import math
import re
from mylib.aoc_frame2 import Day


def parse(text: str):
    """ Compute something from text, as basis for both parts """
    instruction_str, network_str = text.split("\n\n")  # str, str
    instructions = [0 if c == "L" else 1 for c in instruction_str]
    network = dict()
    sources = []
    destinations = set()
    for line in network_str.splitlines():
        src, d0, d1 = re.findall(r"[0-9A-Z]+", line)
        network[src] = (d0, d1)

        if src[-1] == "A":
            sources.append(src)
        if d0[-1] == "Z":
            destinations.add(d0)
        if d1[-1] == "Z":
            destinations.add(d1)
    return instructions, network, sources, destinations


def iter_till_destination(p, network, instruction_iter, destinations):
    for i in itertools.count(1):
        instr = next(instruction_iter)
        p = network[p][instr]
        if p in destinations:
            return i, p


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        instructions, network, _, _ = parse(text)
        instruction_iter = itertools.cycle(instructions)
        i, p = iter_till_destination("AAA", network, instruction_iter, {"ZZZ"})
        return i

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 2, "example1"


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        instructions, network, sources, destinations = parse(text)

        p_first = []
        p_loop_length = []
        for source_nr, p in enumerate(sources):
            instruction_iter = itertools.cycle(instructions)
            i, p = iter_till_destination(p, network, instruction_iter, destinations)
            p_first.append(i)
            i, p = iter_till_destination(p, network, instruction_iter, destinations)
            p_loop_length.append(i)
            # The following is just to verify that we reached a stable loop.
            # The input has the necessary property, but this is not guaranteed by the
            # problem description.
            i, p = iter_till_destination(p, network, instruction_iter, destinations)
            assert i == p_loop_length[-1]

        # Check the assertion, that the steps to the loop and the length of the loop
        # are always pairwise equal.
        assert all(f == l for f, l in zip(p_first, p_loop_length))

        # Based on the assumption above, we can just use the lcm and do not need the
        # Chinese Remainder theorem.
        return math.lcm(*p_first)

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example2, "config"), 6, "example2"


example1 = '''
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
'''


example2 = '''
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''

Day.do_day(day=8, year=2023, part_a=PartA, part_b=PartB)
