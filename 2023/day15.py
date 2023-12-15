from mylib.aoc_frame2 import Day


def holiday_hash(text: str):
    result = 0
    for c in text:
        o = ord(c)
        result += o
        result *= 17
        result = result % 256
    return result


class PartA(Day):
    def compute(self, text, config):
        result = 0
        for s in text.replace("\n", "").split(","):
            result += holiday_hash(s)
        return result

    def tests(self):
        yield holiday_hash("HASH"), 52, "HASH"
        yield self.test_solve("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
                              "config"), 1320, "example"


class PartB(PartA):
    def compute(self, text, config):
        boxes: list[list[tuple[str, int]]] = [[] for i in range(256)]
        for s in text.replace("\n", "").split(","):
            if s[-1] == "-":
                label = s[:-1]
                label_hash = holiday_hash(label)
                boxes[label_hash] = [label_and_length
                                     for label_and_length in boxes[label_hash]
                                     if label_and_length[0] != label]
            else:  # "="
                label = s[:-2]
                label_hash = holiday_hash(label)
                length = int(s[-1])
                box = boxes[label_hash]
                for i, lens_and_length in enumerate(box):
                    if lens_and_length[0] == label:
                        box[i] = (label, length)
                        break
                else:
                    box.append((label, length))

        return sum(
            box_nr * slot_nr * label_and_length[1]
            for box_nr, box in enumerate(boxes, 1)
            for slot_nr, label_and_length in enumerate(box, 1)
            )

    def tests(self):
        yield self.test_solve("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
                              "config"), 145, "example"


Day.do_day(day=15, year=2023, part_a=PartA, part_b=PartB)
