import itertools
from collections import defaultdict
from mylib.aoc_frame2 import Day


def parse(text: str):
    rules = dict()
    inputs = defaultdict(list)
    for rule in text.splitlines():
        left, right_str = rule.split(" -> ")
        if left == "broadcaster":
            m_type = left
            name = left
        else:
            m_type, name = left[0], left[1:]
        destinations = right_str.split(", ")

        rules[name] = (m_type, destinations)
        for destination in destinations:
            inputs[destination].append(name)
    return rules, inputs


def process(module, source, signal, rules, state, sent_pulses):
    sent_pulses[signal] += 1
    if module not in rules:
        return  # unknown module
    m_type, destinations = rules[module]
    if m_type == "%":
        if signal == 1:
            return
        state[module] = 1 - state[module]
        signal_to_send = state[module]
    elif m_type == "&":
        state[module][source] = signal
        all_input_1 = all(signal == 1 for source, signal in state[module].items())
        signal_to_send = 0 if all_input_1 else 1
    elif m_type == "broadcaster":
        signal_to_send = signal
    else:
        raise RuntimeError()
    for destination in destinations:
        yield (destination, module, signal_to_send)


class PartA(Day):
    def compute(self, text, config):
        rules, inputs = parse(text)

        sent_pulses = [0, 0]  # low, high
        state = {module: (
            {source: 0 for source in inputs[module]}
            if rules[module][0] == "&"
            else
            0
        ) for module in inputs.keys() if module in rules}
        for button_i in range(1000):
            # print("--- Button---")
            pulses = [("broadcaster", "button", 0)]
            while pulses:
                module, source, signal = pulses.pop(0)
                pulses.extend(
                    process(module, source, signal, rules, state, sent_pulses))
        return sent_pulses[0] * sent_pulses[1]

    def tests(self):
        yield self.test_solve(example_a1, "config"), 32000000, "example_a1"
        yield self.test_solve(example_a2, "config"), 11687500, "example_a2"


example_a1 = '''
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
'''
example_a2 = '''
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''


class PartB(PartA):
    def compute(self, text, config):
        loops = {"cm": [4091],
                 "gc": [3853],
                 "sz": [4093],
                 "xf": [4073]
                 }
        print("Checking loop assumptions now - as long as you do not interrupt")
        print(loops)

        rules, inputs = parse(text)

        sent_pulses = [0, 0]  # low, high
        state = {module: (
            {source: 0 for source in inputs[module]}
            if rules[module][0] == "&"
            else
            0
        ) for module in inputs.keys() if module in rules}

        for button_i in itertools.count(1):
            pulses = [("broadcaster", "button", 0)]
            pulses_to_rx = [0, 0]
            low_pulses_to_relevant = {module: 0 for module in ["cm", "gc", "sz", "xf"]}
            while pulses:
                module, source, signal = pulses.pop(0)
                if signal == 0 and module in ["cm", "gc", "sz", "xf"]:
                    low_pulses_to_relevant[module] = low_pulses_to_relevant[module] + 1
                if module == "rx":
                    pulses_to_rx[signal] += 1
                pulses.extend(
                    process(module, source, signal, rules, state, sent_pulses))
            if pulses_to_rx[0] == 1:
                # Correct, but takes much too long (262_775_362_119_547)
                return button_i

            # Check the loop assumptions, as long as the program is allowed to run
            for module, loop_lengths in loops.items():
                is_loop_count = False
                for loop_length in loop_lengths:
                    if button_i % loop_length == 0:
                        is_loop_count = True
                if (low_pulses_to_relevant[module] == 1) != is_loop_count:
                    print(button_i, module, low_pulses_to_relevant[module])

            # Result:
            # >>> math.lcm(4091, 3853, 4093, 4073)
            # 262775362119547

    def tests(self):
        return ()


Day.do_day(day=20, year=2023, part_a=PartA, part_b=PartB)
