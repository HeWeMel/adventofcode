import re
from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.text_lines = [re.split(r"[., ]+", line) for line in lines]  # split by separator set

        d.scores = {"Rock": 1, "Paper": 2, "Scissors": 3}
        d.opponent_choices_for_code = {"A": "Rock", "B": "Paper", "C": "Scissors"}

    @staticmethod
    def result_of_second_player(first_choice, second_choice):
        first_wins = {("Rock", "Scissors"), ("Scissors", "Paper"), ("Paper", "Rock")}
        if (first_choice, second_choice) in first_wins:
            return 0
        elif (second_choice, first_choice) in first_wins:
            return 6
        else:
            return 3

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        my_choices_for_code = {"X": "Rock", "Y": "Paper", "Z": "Scissors"}

        total_score = 0
        for line in d.text_lines:
            opponent_code, my_code = line
            opponent_choice = d.opponent_choices_for_code[opponent_code]
            my_choice = my_choices_for_code[my_code]
            result_score = self.result_of_second_player(opponent_choice, my_choice)
            score = d.scores[my_choice] + result_score
            total_score += score
        return total_score

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
A Y
B X
C Z
'''), 15, "example"


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        total_score = 0
        for line in d.text_lines:
            opponent_code, my_code = line
            opponent_choice = d.opponent_choices_for_code[opponent_code]
            for my_choice in ("Rock", "Paper", "Scissors"):
                result_score = self.result_of_second_player(opponent_choice, my_choice)
                if (result_score, my_code) in {(0, "X"), (6, "Z"), (3, "Y")}:
                    break
            score = d.scores[my_choice] + result_score
            total_score += score
        return total_score

    def tests(self):  # yield testcases as tuple: (test_input, correct_result [, test_name])
        yield self.test_solve('''
A Y
B X
C Z
'''), 12, "example"


Day.do_day(day=2, year=2022, part_a=PartA, part_b=PartB)
