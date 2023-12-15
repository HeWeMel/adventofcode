from collections import defaultdict
from mylib.aoc_frame2 import Day


def holiday_hash(text: str):
    result = 0
    for c in text:
        result += ord(c)
        result *= 17
        result = result % 256
    return result


class PartA(Day):
    def compute(self, text, config):
        return sum(holiday_hash(s) for s in text.replace("\n", "").split(","))

    def tests(self):
        yield holiday_hash("HASH"), 52, "HASH"
        yield self.test_solve("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
                              "config"), 1320, "example"


class PartB(PartA):
    def compute(self, text, config):
        # "Dictionaries preserve insertion order. Note that updating a key does not
        #  affect the order. Keys added after deletion are inserted at the end."
        boxes = defaultdict(dict)
        for s in text.replace("\n", "").split(","):
            if s[-1] == "-":
                label = s[:-1]
                length_for_label = boxes[holiday_hash(label)]
                length_for_label.pop(label, None)
            else:  # "="
                label = s[:-2]
                length_for_label = boxes[holiday_hash(label)]
                length = int(s[-1])
                length_for_label[label] = length

        return sum((label_hash + 1) * (slot_nr + 1) * label_and_length[1]
                   for label_hash, length_for_label in boxes.items()
                   for slot_nr, label_and_length in enumerate(length_for_label.items()))

    def tests(self):
        yield self.test_solve("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
                              "config"), 145, "example"


Day.do_day(day=15, year=2023, part_a=PartA, part_b=PartB)
