from mylib.aoc_frame import Day
import re


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        blocks_of_ints = [[int(i) for i in re.findall(r"[0-9]+", block.replace("\n", " "))]
                          for block in text.split("\n\n")]

        d.draws = blocks_of_ints[0]

        d.value_pos_in_block = []  # from block number to dict from value to pos (x, y)
        for block in blocks_of_ints[1:]:
            i_gen = iter(block)
            pos_of_values = {next(i_gen): (x, y) for x in range(5) for y in range(5)}
            d.value_pos_in_block.append(pos_of_values)
        d.player_count = len(d.value_pos_in_block)

    def play(self, d, first_wins):
        winners = set()
        for draw in d.draws:
            for block in range(d.player_count):
                if block in winners:
                    continue
                pos_of_values = d.value_pos_in_block[block]
                pos = pos_of_values.pop(draw, None)
                if pos is not None:
                    col_size = sum(1 for i, (x, y) in pos_of_values.items() if x == pos[0])
                    row_size = sum(1 for i, (x, y) in pos_of_values.items() if y == pos[1])
                    if col_size == 0 or row_size == 0:
                        winners.add(block)
                        if first_wins or len(winners) == d.player_count:
                            return sum(i for i, pos in pos_of_values.items()) * draw
        return None

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, True)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return self.play(d, False)


Day.do_day(day=4, year=2021, part_a=PartA, part_b=PartB)
