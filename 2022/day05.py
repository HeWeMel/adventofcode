from collections import defaultdict
import re
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        pile_text, move_text = text.split("\n\n")

        d.piles = defaultdict(list)
        for line in reversed(pile_text.splitlines()[:-1]):
            column = 0
            while True:
                pile_no_pos = column * 4  + 1
                if pile_no_pos >= len(line):
                    break
                crate = line[pile_no_pos]
                if crate != " ":
                    d.piles[column+1].append(crate)
                column += 1

        d.moves = [[int(n) for n in re.findall(r"[0-9]+", move)]
                   for move in move_text.splitlines()]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for moves, from_pile, to_pile in d.moves:
            for move in range(moves):
                crate = d.piles[from_pile].pop()
                d.piles[to_pile].append(crate)

        return "".join(d.piles[pile].pop() for pile in d.piles.keys())

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''), "CMZ", "example"

class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        for moves, from_pile_no, to_pile_no in d.moves:
            from_pile = d.piles[from_pile_no]
            to_pile = d.piles[to_pile_no]
            crates = from_pile[-moves:]
            del from_pile[-moves:]
            to_pile.extend(crates)

        return "".join(d.piles[pile].pop() for pile in d.piles.keys())

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''), "MCD", "example"


Day.do_day(day=5, year=2022, part_a=PartA, part_b=PartB)
