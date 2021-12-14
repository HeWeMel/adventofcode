import collections
from mylib.aoc_frame import Day


def run(d, runs):
    template, rules = d.text.split("\n\n")

    # A rule replaces a pair of characters by two pairs, by "inserting" a third character
    rules = (line.split(" -> ") for line in rules.splitlines())
    rules = {l: (l[0] + r, r + l[1]) for l, r in rules}

    # The first character of the template will remain in position during all steps, but the
    # calculation based on character pairs will miss it in the end result -> Save it.
    template_first_char = template[0]

    # Replace template by all the character pairs in it, and count those
    template = collections.Counter(template[p:p + 2] for p in range(len(template) - 1))

    for step in range(runs):
        template_new = collections.Counter()
        # Replace pairs by applying rules. Keep pair counts as counts of newly created pairs.
        for pair, count in template.items():
            for new_pairs in rules.get(pair, ()):
                template_new[new_pairs] += count
        template = template_new

    # Count each of the second characters in the pairs, plus the saved first template character.
    counts = collections.Counter({template_first_char: 1})
    for pair, count in template.items():
        counts[pair[1]] += count

    counts = sorted(counts.values())
    return counts[-1] - counts[0]


class PartA(Day):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return run(d, 10)  # 2549


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return run(d, 40)  # 2516901104210


Day.do_day(day=14, year=2021, part_a=PartA, part_b=PartB)
