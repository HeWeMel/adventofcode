import re
from mylib.aoc_frame2 import Day


def parse(text: str):
    """ Extract list of seed integers, and the list of mappings, each as
    list of tuples (dest_range_start, source_range_start, range_len). """
    blocks = text.split("\n\n")
    seeds = [int(n) for n in re.findall(r"[0-9]+", blocks[0])]
    mappings = [[[int(s) for s in line.split()]
                 for line in a_map.splitlines()[1:]]
                for a_map in blocks[1:]]
    return seeds, mappings


def apply_map(i, mapping):
    """ Apply the range mappings to i, and compute, how much higher *i* could be
    without have a result that is equally higher (buffer length) """
    min_from_a_start = float("inf")
    for dest_range_start, source_range_start, range_len in mapping:
        if source_range_start <= i < source_range_start + range_len:
            # *i* is within the mapping range: apply the map, and report distance from
            # upper limit of the source range as buffer length
            return (i - source_range_start + dest_range_start,
                    source_range_start + range_len - i - 1)
        if i >= source_range_start + range_len:
            # If *i* is higher than the upper source limit, we neither have to apply
            # a map nor do we get an upper limit from this map
            continue
        # if *i* is lower than the lower source limit, we do not have to apply
        # a map, but we get the distance from the lower limit as buffer length
        # limit. If the new limit is lower than the previous one, save it
        min_from_a_start = min(min_from_a_start, source_range_start - i)
    return i, min_from_a_start


class PartA(Day):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        seeds, mappings = parse(text)
        min_loc = float("inf")
        for i in seeds:
            for mapping in mappings:
                i, _ = apply_map(i, mapping)
            if i < min_loc:
                min_loc = i

        return min_loc

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 35, "example1"


class PartB(PartA):
    def compute(self, text, config):
        """ Return result for puzzle *text* and *config*"""
        seeds, mappings = parse(text)
        min_loc = float("inf")
        for j in range(0, len(seeds), 2):
            seed, seed_range_len = seeds[j:j+2]
            seed_range_end = seed + seed_range_len
            while seed < seed_range_end:
                # Apply the mapping to the seed number, and compute the minimum
                # number by that we could go higher than seed without just getting
                # equally higher results
                i = seed
                min_ok_range = float("inf")
                for mapping in mappings:
                    i, ok_range_len = apply_map(i, mapping)
                    if ok_range_len < min_ok_range:
                        min_ok_range = ok_range_len
                if i < min_loc:
                    min_loc = i
                # Jump behind the range of seed numbers that can just give
                # higher and higher results
                seed += min_ok_range + 1
        return min_loc

    def tests(self):
        """ Yield testcases as tuple: (test_result, correct_result [, test_name]) """
        yield self.test_solve(example1, "config"), 46, "example2"


example1 = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

Day.do_day(day=5, year=2023, part_a=PartA, part_b=PartB)
