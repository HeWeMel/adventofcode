from mylib.aoc_frame2 import Day


def parse(text: str):
    workflows_str, parts_str = text.split("\n\n")
    workflows = dict()
    for workflow_str in workflows_str.splitlines():
        name, rules_str = workflow_str.split("{")
        rules_str_with_default = rules_str[:-1]
        rules_str, default_workflow = rules_str_with_default.rsplit(",", 1)

        rules = []
        for rule_str in rules_str.split(","):
            left, to_workflow = rule_str.split(":")
            attr, relation, value_str = left[0], left[1], left[2:]
            rules.append((attr, relation, int(value_str), to_workflow))
        workflows[name] = (rules, default_workflow)
    parts = [{valuation[0]: int(valuation[2:])
              for valuation in part_str[1:-1].split(",")
              } for part_str in parts_str.splitlines()]
    return workflows, parts


def follow(part, workflow, workflows, next_trigger_for_attr):
    """ Follow *part* through the *workflows* till acceptance or rejection,
    and return this result. For each attribute used during the process, compute
    the next following value for that the workflow decisions will change.
    """
    while workflow not in "AR":
        rules, default_workflow = workflows[workflow]
        for attr, relation, value, to_workflow in rules:
            if relation == "<":
                if part[attr] < value:
                    if (attr not in next_trigger_for_attr
                            or value < next_trigger_for_attr[attr]):
                        next_trigger_for_attr[attr] = value
                    workflow = to_workflow
                    break
            else:
                if part[attr] > value:
                    workflow = to_workflow
                    break
                if (attr not in next_trigger_for_attr
                        or value + 1 < next_trigger_for_attr[attr]):
                    next_trigger_for_attr[attr] = value + 1
        else:
            workflow = default_workflow
    return workflow


class PartA(Day):
    def compute(self, text, config):
        workflows, parts = parse(text)
        return sum(
            sum(part[attr] for attr in "xmas")
            if follow(part, "in", workflows, dict()) == "A" else 0
            for part in parts)

    def tests(self):
        yield self.test_solve(example_a1, "config"), 19114, "example1_1"


def accepted_combinations(valuation, names, workflows):
    """ Recursively add valuations for the attributes *names* to *valuation*
    and compute the number such valuations leading to acceptance of such a
    'part'. For each attribute used during occurring workflow processes, compute
    the next following value for that the workflow decisions will change. """
    if not len(names):
        next_trigger_for_attr = dict()
        result = follow(valuation, "in", workflows, next_trigger_for_attr)
        return 1 if result == "A" else 0, next_trigger_for_attr

    name, names = names[0], names[1:]
    # Try out relevant values *v* for attribute *name*
    v = 1
    next_trigger_for_all_attr = dict()
    r = 0  # The result is aggregated here
    prev_v = 0  # The previous value of v before the most recent jump
    prev_recursive_result = 0  # The recursive result for "valuation | {name: v}"
    while v < 4001:
        # Valuations multiplied by number of values of v since prev_v, i.e.,
        # "how long" in terms of v these valuations hold.
        r += prev_recursive_result * (v - prev_v)
        # Try valuation with next relevant value for v
        prev_recursive_result, next_trigger_for_attr = accepted_combinations(
            valuation | {name: v}, names, workflows)
        # Take new information about next trigger values to the aggregated infos
        for key, trigger_value in next_trigger_for_attr.items():
            if (key not in next_trigger_for_all_attr
                    or trigger_value < next_trigger_for_all_attr[key]):
                next_trigger_for_all_attr[key] = trigger_value
        # Save v before jumping to the next relevant value
        prev_v = v
        if name not in next_trigger_for_attr:
            # The complete attribute *name* is irrelevant for the recursive result.
            break
        # Jump to next relevant value for v, or the end, if there is none
        v = min(next_trigger_for_attr[name], 4001)
    # Take in the results for the last jump up to (lower than) 4001
    r += prev_recursive_result * (4001 - prev_v)
    return r, next_trigger_for_all_attr


class PartB(PartA):
    def compute(self, text, config):
        workflows, parts = parse(text)
        r, all_attrs = accepted_combinations(dict(), "xmas", workflows)
        return r

    def tests(self):
        yield self.test_solve(example_a1, "config"), 167409079868000, "example2"


example_a1 = '''
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''

Day.do_day(day=19, year=2023, part_a=PartA, part_b=PartB)
