from dataclasses import dataclass


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()

    grid = []
    for line in content:
        grid.append(list(line))

    rows, cols = grid_size(grid)
    for i in range(cols):
        for j in range(rows):
            character = grid[j][i]
            grid[j][i] = Element(character, previous=[])

    return grid


@dataclass
class Element:
    character: str
    previous: list
    visited: bool = False


@dataclass
class Beam:
    i: int
    j: int
    direction: str  # NESW


def grid_size(grid: list) -> (int, int):
    rows = len(grid)
    cols = len(grid[0])

    return rows, cols


def move_beam(beam: Beam, grid: list) -> bool:
    """
    move the beam to the new position:
    adjust beam location (i, j)
    return False if the beam has reached the edge of the grid
    return True otherwise: the beam has actually moved
    """
    rows, cols = grid_size(grid)
    direction = beam.direction
    i, j = beam.i, beam.j

    beam_has_moved = False
    valid_move = False

    match direction:
        case 'N':
            if beam.j >= 1:
                beam.j -= 1
                valid_move = True
        case "S":
            if beam.j <= rows - 2:
                beam.j += 1
                valid_move = True
        case "E":
            if beam.i <= cols - 2:
                beam.i += 1
                valid_move = True
        case "W":
            if beam.i >= 1:
                beam.i -= 1
                valid_move = True

    if valid_move:
        new_position: Element = grid[beam.j][beam.i]
        new_position.visited = True
        previous_position = [i, j, direction]
        if previous_position in new_position.previous:
            pass
        else:
            new_position.previous.append(previous_position)
            beam_has_moved = True

    return beam_has_moved


def rotate_beam_direction(beam: Beam, grid: list):
    """evaluates beam position and return a second beam of None"""
    direction = beam.direction
    i, j = beam.i, beam.j
    element: Element = grid[j][i]
    character = element.character

    match character:
        case ".":
            pass
        case "\\":
            match direction:
                case "N":
                    beam.direction = "W"
                case "S":
                    beam.direction = "E"
                case "E":
                    beam.direction = "S"
                case "W":
                    beam.direction = "N"
        case "/":
            match direction:
                case "N":
                    beam.direction = "E"
                case "S":
                    beam.direction = "W"
                case "E":
                    beam.direction = "N"
                case "W":
                    beam.direction = "S"
        case "|":
            match direction:
                case "N":
                    pass
                case "S":
                    pass
                case "E":
                    beam.direction = "N"  # + extra beam S
                    second_beam = Beam(i, j, "S")
                    return second_beam
                case "W":
                    beam.direction = "N"  # + extra beam S
                    second_beam = Beam(i, j, "S")
                    return second_beam
        case "-":
            match direction:
                case "E":
                    pass
                case "W":
                    pass
                case "N":
                    beam.direction = "E"  # + extra beam W
                    second_beam = Beam(i, j, "W")
                    return second_beam

                case "S":
                    beam.direction = "E"  # + extra beam W
                    second_beam = Beam(i, j, "W")
                    return second_beam

    return None


def print_grid(grid: list) -> None:
    rows, cols = grid_size(grid)
    for j in range(rows):
        for i in range(cols):
            element: Element = grid[j][i]
            if element.visited:
                print("#", end="")
            else:
                print(".", end="")
        print()


def count_tiles(grid: list) -> int:
    rows, cols = grid_size(grid)
    number_of_energized_tiles = 0
    for j in range(rows):
        for i in range(cols):
            element: Element = grid[j][i]
            if element.visited:
                number_of_energized_tiles += 1

    return number_of_energized_tiles


def compute_part_one(file_name: str) -> int:
    grid = read_input_file(file_name)

    beam = Beam(0, 0, 'E')
    rotate_beam_direction(beam, grid)  # the beam might have to change direction immediately
    element: Element = grid[beam.j][beam.i]
    element.visited = True

    beam_queue = [beam]
    while beam_queue:
        beam = beam_queue.pop()
        beam_has_moved = True
        while beam_has_moved:
            beam_has_moved = move_beam(beam, grid)
            if not beam_has_moved:
                break
            new_beam = rotate_beam_direction(beam, grid)
            if new_beam is not None:
                beam_queue.append(new_beam)
    # print_grid(grid)
    number_of_tiles = count_tiles(grid)
    print(f'{number_of_tiles= }')

    return number_of_tiles


def compute_part_two(file_name: str) -> int:
    """
    make a list of starting beams and loop through them all to find the maximum
    for each cycle in the loop, reset the grid
    element.visited reset to False
    element.previous reset to []
    (alternative: re-read the input each cycle
    """
    grid = read_input_file(file_name)
    rows, cols = grid_size(grid)
    starting_beams = []
    for i in range(cols):
        beam = Beam(i, 0, 'S')
        starting_beams.append(beam)
        beam = Beam(i, rows-1, 'N')
        starting_beams.append(beam)

    for j in range(rows):
        beam = Beam(0, j, 'E')
        starting_beams.append(beam)
        beam = Beam(cols-1, j, 'W')
        starting_beams.append(beam)

    max_number_of_tiles = 0
    for beam in starting_beams:
        grid = read_input_file(file_name)
        element: Element = grid[beam.j][beam.i]
        element.visited = True
        beam_queue = [beam]
        while beam_queue:
            beam = beam_queue.pop()
            beam_has_moved = True
            while beam_has_moved:
                new_beam = rotate_beam_direction(beam, grid)
                if new_beam is not None:
                    beam_queue.append(new_beam)
                beam_has_moved = move_beam(beam, grid)
                if not beam_has_moved:
                    break
        number_of_tiles = count_tiles(grid)
        max_number_of_tiles = max(max_number_of_tiles, number_of_tiles)
        print(f'{number_of_tiles= }')

    return max_number_of_tiles


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input16.txt')}")
    print(f"Part II: {compute_part_two('input/input16.txt')}")
