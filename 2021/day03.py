from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.words = text.splitlines()

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        l = len(d.words)
        gamma_gen = (str(int(sum(int(i[b]) for i in d.words) > l // 2)) for b in range(12))
        gamma = int("".join(gamma_gen), 2)
        epsilon = 2**12-1 - gamma
        return gamma * epsilon


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        def result(more_ones):
            lst = d.words[:]
            for b in range(12):
                l = len(lst)
                c1 = sum(int(i[b]) for i in lst)
                bit = "1" if ((l//2 <= c1) == more_ones) else "0"
                lst = [i for i in lst if i[b] == bit]
                if len(lst) == 1:
                    break
            return int(lst[0], 2)
        return result(True) * result(False)


Day.do_day(day=3, year=2021, part_a=PartA, part_b=PartB)
