from mylib.aoc_frame import Day, multiply_list


class PartA(Day):
    def parse(self, text, d):  # store puzzle parsing result data into attributes of d
        d.bits = "".join("{0:0>4b}".format(int(n, 16)) for n in text.splitlines()[0])

    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d.bits)[1]

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve('''38006F45291200'''), 1+6+2
        yield self.test_solve('''8A004A801A8002F478'''), 16
        yield self.test_solve('''620080001611562C8802118E34'''), 12
        yield self.test_solve('''A0016C880162017C3686B18A3D4780'''), 31


class PartB(PartA):
    def compute(self, d):  # return puzzle result, get parsing data from attributes of d
        return do(d.bits)[0]

    def tests(self):  # yield testcases as tuple: (test_result, correct_result [, test_name])
        yield self.test_solve('''C200B40A82'''), 3
        yield self.test_solve('''04005AC33890'''), 54
        yield self.test_solve('''880086C3E88112'''), 7
        yield self.test_solve('''CE00C43D881120'''), 9
        yield self.test_solve('''D8005AC2A8F0'''), 1
        yield self.test_solve('''F600BC2D8F'''), 0
        yield self.test_solve('''9C005AC2F8F0'''), 0
        yield self.test_solve('''9C0141080250320F1802104A08'''), 1


def do(bits):  # returns computed value, total of versions, remaining bits
    def read(count):
        nonlocal bits
        my_bits = bits[:count]
        bits = bits[count:]
        return my_bits

    def read_int(count):
        return int(read(count), 2)

    version = read_int(3)
    type_id = read_int(3)

    if type_id == 4:  # literal
        val_bits = ""
        while True:
            last_marker = read_int(1)
            val_bits += read(4)
            if last_marker == 0:
                return int(val_bits, 2), version, bits
    # op
    total = version
    results = []
    if read_int(1) == 0:  # mode
        sub_bits = read(read_int(15))
        while len(sub_bits) > 0:
            v, sub_total, sub_bits = do(sub_bits)
            total += sub_total
            results.append(v)

    else:
        for i in range(read_int(11)):
            v, sub_total, bits = do(bits)
            total += sub_total
            results.append(v)

    result = sum(results) if type_id == 0 else\
        multiply_list(results) if type_id == 1 else\
        min(results) if type_id == 2 else\
        max(results) if type_id == 3 else\
        (1 if results[0] > results[1] else 0) if type_id == 5 else\
        (1 if results[0] < results[1] else 0) if type_id == 6 else\
        (1 if results[0] == results[1] else 0) if type_id == 7 else \
        None
    return result, total, bits


Day.do_day(day=16, year=2021, part_a=PartA, part_b=PartB)
