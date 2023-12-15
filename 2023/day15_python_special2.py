import itertools
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
        """ Notes from Python documentation:
        - "Dictionaries preserve insertion order. Note that updating a key does not
           affect the order. Keys added after deletion are inserted at the end."
        - "The built-in sorted() function is guaranteed to be stable." """
        boxes = dict[str, int]()
        for s in text.replace("\n", "").split(","):
            if s[-1] == "-":
                boxes.pop(s[:-1], None)
            else:  # "="
                boxes[s[:-2]] = int(s[-1])

        def label_hash(boxes_item: tuple[str, int]):
            return holiday_hash(boxes_item[0])

        return sum((label_hash + 1) * (slot_nr + 1) * label_and_length[1]
                   for label_hash, label_and_length_iter in
                   itertools.groupby(sorted(boxes.items(), key=label_hash), key=label_hash)
                   for slot_nr, label_and_length in enumerate(label_and_length_iter))

    def tests(self):
        yield self.test_solve("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7",
                              "config"), 145, "example"


Day.do_day(day=15, year=2023, part_a=PartA, part_b=PartB)
