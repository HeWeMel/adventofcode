import re
from mylib.aoc_frame import Day


def do(xv, yv, xtmin, xtmax, ytmin, ytmax):
    # Parameters: Start velocity x and y, min and max coordinates x and y of target.
    #   For x velocity, xtmax + 1 is a save upper bound.
    #   For y velocity, ytmin - 1 is a save lower bound.
    # If goal has been hit, returns highest height and None.
    # If goal has been missed, returns -1 and x coordinate of highest point.
    xp = yp = 0
    ymax = ymaxx = -1
    while xp <= xtmax and yp >= ytmin:  # stop when right of goal or lower than goal
        if yp > ymax:  # keep highest point
            ymax, ymaxx = yp, xp
        if xtmin <= xp <= xtmax and ytmin <= yp <= ytmax:  # goal hit
            return ymax, None
        xp, yp, xv, yv = xp + xv, yp + yv, xv - 1 if xv > 0 else xv, yv - 1
    return -1, ymaxx


class PartA(Day):
    def parse(self, text, d):
        d.xmin, d.xmax, d.ymin, d.ymax = [int(n) for n in re.findall(r"[0-9-]+", text)]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return max(do(xv, yv, d.xmin, d.xmax, d.ymin, d.ymax)[0]
                   for xv in range(1, d.xmax + 1) for yv in range(d.ymin - 1, 1000))


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        r = 0
        for yv in range(d.ymin - 1, 1000):
            for xv in range(1, d.xmax + 1):
                my, myx = do(xv, yv, d.xmin, d.xmax, d.ymin, d.ymax)
                if myx is None:
                    r += 1  # count hits
                else:
                    if myx > d.xmax:
                        break  # stop raising x velocity if highest point is already right of goal
        return r


Day.do_day(day=17, year=2021, part_a=PartA, part_b=PartB)
