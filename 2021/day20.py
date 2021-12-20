from mylib.aoc_frame import Day


def go(alg, img, steps):
    light, dark = "#."
    for step in range(steps):
        height, width = len(img), len(img[0])
        environment = light if alg[0] == "#" and step % 2 == 1 else dark

        new_img = []
        for yp in range(-1, height+1):
            x_str = ""
            for xp in range(-1, width+1):
                b = 0
                for yd in range(-1, 2):
                    for xd in range(-1, 2):
                        y, x = yp + yd, xp + xd
                        v = img[y][x] if 0 <= x < width and 0 <= y < height else environment
                        b = b * 2 + (v == light)
                x_str += alg[b]
            new_img.append(x_str)
        img = new_img

    lit = sum((img[y][x] == light) for x in range(len(img[0])) for y in range(len(img)))
    return lit


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        lines = text.splitlines()
        d.alg, d.img = lines[0], lines[2:]

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return go(d.alg, d.img, 2)


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return go(d.alg, d.img, 50)


Day.do_day(day=20, year=2021, part_a=PartA, part_b=PartB)
