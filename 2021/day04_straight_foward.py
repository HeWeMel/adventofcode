from mylib.aoc_frame import Day
import re


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        blocks_of_ints = [[int(i) for i in re.findall(r"[0-9]+", block.replace("\n", " "))]
                          for block in text.split("\n\n")]

        d.draws = blocks_of_ints[0]

        d.values = []
        for block in blocks_of_ints[1:]:
            i_gen = iter(block)
            values = [[next(i_gen) for x in range(5)] for x in range(5)]
            d.values.append(values)
        d.player_count = len(d.values)

    def play(self, d, first_wins):
        winners = set()
        for draw in d.draws:
            for block in range(d.player_count):
                if block in winners:
                    continue
                values = d.values[block]
                found = [(x, y) for x in range(5) for y in range(5) if values[y][x] == draw]
                if len(found) == 0:
                    continue
                xf, yf = found[0]
                values[yf][xf] = None
                col_size = sum(1 for y in range(5) if values[y][xf] is not None)
                row_size = sum(1 for x in range(5) if values[yf][x] is not None)
                if col_size == 0 or row_size == 0:
                    winners.add(block)
                    if first_wins or len(winners) == d.player_count:
                        return sum(values[y][x]
                                   for x in range(5)
                                   for y in range(5)
                                   if values[y][x] is not None) * draw
        return None

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, False)


Day.do_day(day=4, year=2021, part_a=PartA, part_b=PartB)
