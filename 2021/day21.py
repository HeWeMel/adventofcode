import functools
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        text = text.splitlines()
        d.start_positions = int(text[0][-1]), int(text[1][-1])

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        position_player1, position_player2 = d.start_positions[0], d.start_positions[1]
        dice_rolls = score_player1 = score_player2 = 0

        def roll_dice():
            while True:
                for v in range(1, 101):
                    yield v
        dice = iter(roll_dice())

        while True:
            position_player1 += next(dice) + next(dice) + next(dice)
            while position_player1 > 10:
                position_player1 -= 10
            dice_rolls += 3
            score_player1 += position_player1
            if score_player1 >= 1000:
                return dice_rolls * score_player2
            position_player1, position_player2, score_player1, score_player2 = \
                position_player2, position_player1, score_player2, score_player1


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        wins = do((d.start_positions[0], 0), (d.start_positions[1], 0))
        return max(wins)


@functools.cache
def do(pos_and_score1, pos_and_score2):
    wins = [0, 0]
    for d1 in range(1, 4):
        for d2 in range(1, 4):
            for d3 in range(1, 4):
                pos, score = pos_and_score1
                pos += d1 + d2 + d3
                while pos > 10:
                    pos -= 10
                score += pos
                if score >= 21:
                    wins[0] += 1
                else:
                    found_wins = do(pos_and_score2, (pos, score))  # player in parameters exchanged
                    wins[1] += found_wins[0]  # found wins of recursive exchanged
                    wins[0] += found_wins[1]
    return wins


Day.do_day(day=21, year=2021, part_a=PartA, part_b=PartB)
