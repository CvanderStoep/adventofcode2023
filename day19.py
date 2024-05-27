from dataclasses import dataclass
from typing import Optional


@dataclass
class Part:
    x: int = 0
    m: int = 0
    a: int = 0
    s: int = 0


@dataclass
class Solution:
    x: list
    m: list
    a: list
    s: list


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

    def is_leaf(step: str) -> bool:
        return len(step) == 1

    def check_leaf(step: str) -> bool:
        return step == "A"

    for step in workflow:
        if is_leaf(step):
            return check_leaf(step)

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


def process_solution(solution: Solution, workflows: dict, start: str, valid_solutions: list) -> list:
    """processes the solution based on the workflow and returns the solution stack"""

    print(f'{start= }')
    workflow = workflows[start]
    # valid_solutions = []

    for step in workflow:
        if step == "A":
            valid_solutions.append(solution)
        elif step == "R":
            continue
        elif ":" in step:
            x, m, a, s = 1000, 1000, 1000, 1000  # TODO modify
            expr, action = step.split(":")  # s<1351:px
            if eval(expr):
                if action == "A":
                    x = solution.x.copy()
                    m = solution.m.copy()
                    a = solution.a.copy()
                    s = solution.s.copy()
                    s = [1, 1351]
                    new_solution = Solution(x, m, a, s)
                    valid_solutions.append(new_solution)  # TODO modify solution range
                elif action == "R":
                    continue
                else:
                    pass
                # process_solution(solution, workflows, start=step)  # TODO modify solution
        else:  # process new workflow
            process_solution(solution, workflows, start=step, valid_solutions=valid_solutions)

    return valid_solutions


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


def compute_part_two(file_name: str) -> int:
    workflows, parts = read_input_file(file_name)
    start = "in"
    valid_solutions = []

    solution = Solution([1, 4000], [1, 4000], [1, 4000], [1, 4000])
    output = process_solution(solution, workflows, start, valid_solutions)
    print(f'{output= }')
    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input19.txt')}")
    print(f"Part II: {compute_part_two('input/input19.txt')}")
