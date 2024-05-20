from dataclasses import dataclass


@dataclass
class Part:
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0


def read_input_file(file_name: str) -> tuple:
    """
    :param file_name:
    :return: dictionary with workflows, list with parts
    """
    with open(file_name) as f:
        content1, content2 = f.read().split("\n\n")

    # px{a<2006:qkq,m>2090:A,rfg}
    content1 = content1.splitlines()
    workflows = dict()
    for line in content1:
        items = line.split("{")
        name = items[0]
        rules = items[1][:-1].split(',')
        workflows.update({name: rules})

    # {x=787,m=2655,a=1222,s=2876}
    content2 = content2.splitlines()
    parts = []
    for line in content2:
        part = line[1:-1].split(",")
        new_part = Part()
        for rating in part:
            r, number = rating.split("=")
            if r == "x":
                new_part.x = int(number)
            if r == "m":
                new_part.m = int(number)
            if r == "a":
                new_part.a = int(number)
            if r == "s":
                new_part.s = int(number)
        parts.append(new_part)

    return workflows, parts


def process_workflow(workflows: dict, start: str, part: Part) -> bool:
    """processes the part based on the workflow and return True if the part is accepted"""

    workflow = workflows[start]

    for step in workflow:
        if step == "A":
            return True
        if step == "R":
            return False
        if ":" in step:
            x, m, a, s = part.x, part.m, part.a, part.s
            expr, action = step.split(":")  # s<1351:px
            if eval(expr):
                if action == "A":
                    return True
                if action == "R":
                    return False
                return process_workflow(workflows, start=action, part=part)
        else:
            return process_workflow(workflows, start=step, part=part)

    return True


def sum_part_rating(part: Part) -> int:

    return part.x + part.m + part.a + part.s


def compute_part_one(file_name: str) -> int:
    workflows, parts = read_input_file(file_name)

    start = "in"
    sum_all_part_rating = 0
    for part in parts:
        outcome = process_workflow(workflows, start, part)
        if outcome:
            sum_all_part_rating += sum_part_rating(part)

    print(f'{sum_all_part_rating= }')

    return sum_all_part_rating


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input19.txt')}")
    # print(f"Part II: {compute_part_two('input/input19.txt')}")
