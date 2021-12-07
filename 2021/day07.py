from mylib.aoc_frame import Day


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.list = [int(n) for n in text.split(",")]  # 0,1,2,3

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        d.list.sort()
        p = d.list[len(d.list) // 2]
        f = sum(abs(s - p) for s in d.list)
        return f


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        def fuel(dist): return dist * (dist + 1) // 2

        min_c = min(d.list)
        max_c = max(d.list)
        f_min = fuel(max_c - min_c) * len(d.list)
        for p in range(min_c, max_c + 1):
            f = sum(fuel(abs(s - p)) for s in d.list)
            if f < f_min:
                f_min = f
        return f_min


Day.do_day(day=7, year=2021, part_a=PartA, part_b=PartB)
