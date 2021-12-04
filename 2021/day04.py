from mylib.aoc_frame import Day
import re


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        blocks_of_ints = [[int(i) for i in re.findall(r"[0-9]+", block.replace("\n", " "))]
                       for block in text.split("\n\n")]

        d.draws = blocks_of_ints[0]

        d.numbers = []  # from block number to numbers in block
        d.rows_and_columns = []  # from block number to row and number sets withs their numbers

        for block in blocks_of_ints[1:]:
            i_gen = (i for i in block)

            columns = [set() for i in range(5)]
            rows = [set() for i in range(5)]
            fields = set()
            for y in range(5):
                for x in range(5):
                    i = next(i_gen)
                    fields.add(i)
                    columns[x].add(i)
                    rows[y].add(i)
            d.numbers.append(fields)
            d.rows_and_columns.append(columns + rows)
        d.player_count = len(d.numbers)

    def play(self, d, first_wins):
        winners = set()
        for draw in d.draws:
            for block in range(d.player_count):
                if block in winners:
                    continue
                d.numbers[block].discard(draw)
                for group in d.rows_and_columns[block]:
                    group.discard(draw)
                    if len(group) == 0:
                        winners.add(block)
                        if first_wins or len(winners) == d.player_count:
                            return sum(i for i in d.numbers[block]) * draw
        return None

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, False)


Day.do_day(day=4, year=2021, part_a=PartA, part_b=PartB)
