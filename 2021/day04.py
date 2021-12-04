from mylib.aoc_frame import Day
import re


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        blocks = [block.replace("\n", " ") for block in text.split("\n\n")]
        d.draws = [int(i) for i in blocks[0].split(",")]
        boards = blocks[1:]

        d.blocks_ints = []
        d.columns_ints = []
        d.rows_ints = []

        for block in boards:
            i_gen = (int(i) for i in re.findall(r"[0-9]+", block))

            columns = [set() for i in range(5)]
            rows = [set() for i in range(5)]
            fields = set()
            for y in range(5):
                for x in range(5):
                    i = next(i_gen)
                    fields.add(i)
                    columns[x].add(i)
                    rows[y].add(i)
            d.blocks_ints.append(fields)
            d.columns_ints.append(columns)
            d.rows_ints.append(rows)
        d.player_count = len(d.blocks_ints)

    def play(self, d, first_wins):
        winners = set()
        for draw in d.draws:
            for block in range(len(d.blocks_ints)):
                if block in winners:
                    continue
                d.blocks_ints[block].discard(draw)
                for c in range(5):
                    d.columns_ints[block][c].discard(draw)
                    d.rows_ints[block][c].discard(draw)
                    if len(d.columns_ints[block][c]) == 0 or len(d.rows_ints[block][c]) == 0:
                        winners.add(block)
                        if first_wins or len(winners) == d.player_count:
                            return sum(i for i in d.blocks_ints[block]) * draw
        return None

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, False)


Day.do_day(day=4, year=2021, part_a=PartA, part_b=PartB)
