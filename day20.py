def read_input_file(file_name: str) -> tuple:
    with open(file_name) as f:
        content = f.read().splitlines()

    modules = dict()
    for line in content:
        items = line.split(" -> ")
        if items[0] == 'broadcaster':
            module_type = 'broadcast'
            name = items[0]
        elif items[0][0] == "%":
            module_type = "flip-flop"
            name = items[0][1:]
        else:
            module_type = "inverter"
            name = items[0][1:]
        destination = items[1].split(',')
        destination = [a.strip() for a in destination]
        module = (module_type, destination)
        modules.update({name: module})

    return modules


def compute_part_one(file_name: str) -> int:
    output = read_input_file(file_name)
    print(output['a'])

    print(output)


    return 0


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input20.txt')}")
    # print(f"Part II: {compute_part_two('input/input20.txt')}")
