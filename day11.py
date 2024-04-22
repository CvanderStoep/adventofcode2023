# import queue
from dataclasses import dataclass
from itertools import combinations

# import re

"""
---> i (x)
|
j(y)  image[j][i]
|

data model:
image[j][i] = consists of empty space(.) and galaxy(#)
"""


@dataclass
class Galaxy:
    i: int
    j: int


def read_input_file(file_name: str) -> list:
    # pattern = r"[+-]?\d+"
    image = []

    with open(file_name) as f:
        content = f.read().splitlines()

    for line in content:
        image.append(list(line))

    return image


def image_to_galaxies(image) -> list:
    rows, cols = image_size(image)
    galaxies = []
    for j in range(rows):
        for i in range(cols):
            # if image[j] == ["."] * cols:
            if image[j][i] == "#":
                galaxy = Galaxy(i, j)
                galaxies.append(galaxy)
    return galaxies


def empty_spaces(image) -> tuple[list, list]:
    """check for empty spaces in the image and return the lists of empty rows and cols"""
    rows, cols = image_size(image)
    empty_rows = []
    empty_cols = []
    for j in range(rows):
        if image[j] == ["."] * cols:
            empty_rows.append(j)
    for i in range(cols):
        col = [image[j][i] for j in range(rows)]
        if col == ["."] * rows:
            empty_cols.append(i)

    return empty_rows, empty_cols


def expand_galaxies(image):
    """
    expands the existing galaxies based on empty rows/cols
    updates the x,y coordinates of each galaxy object
    """
    rows, cols = image_size(image)
    empty_rows, empty_cols = empty_spaces(image)

    new_image = []

    for j in range(rows):
        row = []
        for i in range(cols):
            row.append(image[j][i])
            if i in empty_cols:
                row.append(image[j][i])

        new_image.append(row)
        if j in empty_rows:
            new_image.append(row)

    return new_image


def expand_galaxies2(image):
    """
    expands the existing galaxies based on empty rows/cols
    updates the x,y coordinates of each galaxy object
    """
    rows, cols = image_size(image)
    empty_rows, empty_cols = empty_spaces(image)
    image_multiplier = 1_000_000

    galaxies = image_to_galaxies(image)
    new_galaxies = []
    for galaxy in galaxies:
        i = galaxy.i
        j = galaxy.j
        new_galaxy = Galaxy(i, j)
        new_galaxies.append(new_galaxy)

    for i in empty_cols:
        for g, n_g in zip(galaxies, new_galaxies):
            if g.i > i:
                n_g.i += (image_multiplier - 1)
    for j in empty_rows:
        for g, n_g in zip(galaxies, new_galaxies):
            if g.j > j:
                n_g.j += (image_multiplier - 1)

    return new_galaxies


def print_image(image):
    """prints the full grid"""
    rows, cols = image_size(image)
    for j in range(rows):  # rows
        for i in range(cols):  # cols
            print(image[j][i], end="")
        print()


def image_size(image) -> (int, int):
    rows = len(image)
    cols = len(image[0])

    return rows, cols


def galaxy_distance(galaxy1: Galaxy, galaxy2: Galaxy) -> int:
    distance = abs(galaxy2.i - galaxy1.i) + abs(galaxy2.j - galaxy1.j)

    return distance


def compute_part_one(file_name: str) -> int:
    image = read_input_file(file_name)
    image = expand_galaxies(image)  # explode empty rows/cols
    galaxies = image_to_galaxies(image)  # convert image to list of galaxies

    sum_paths = 0
    for g1, g2 in combinations(galaxies, 2):
        sum_paths += galaxy_distance(g1, g2)

    return sum_paths


def compute_part_two(file_name: str) -> int:
    image = read_input_file(file_name)
    galaxies = expand_galaxies2(image)  # explode empty rows/cols

    sum_paths = 0
    for g1, g2 in combinations(galaxies, 2):
        sum_paths += galaxy_distance(g1, g2)

    return sum_paths


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input11.txt')}")
    print(f"Part II: {compute_part_two('input/input11.txt')}")
