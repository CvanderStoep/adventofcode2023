import re
from dataclasses import dataclass


@dataclass
class Card:
    winning_numbers: list
    my_numbers: list
    quantity: int


def read_input_file(file_name: str) -> list:
    with open(file_name) as f:
        content = f.read().splitlines()
    cards = []
    for line in content:
        numbers = line.split(":")[1].split("|")
        winning_numbers = re.findall(r'(\d+)', numbers[0])
        my_numbers = re.findall(r'(\d+)', numbers[1])
        card = Card(winning_numbers, my_numbers, quantity=1)
        cards.append(card)

    return cards


def compute_part_two(list_of_numbers: list) -> int:
    running_number_of_scratch_cards = [1]*len(list_of_numbers)
    max_index = len(running_number_of_scratch_cards)
    for i in range(len(list_of_numbers)):
        # for j in range(i+1, i + 1 + list_of_numbers[i]): # DONE check maximum index of j, can run out of bounds
        for j in range(i + 1, min(i + 1 + list_of_numbers[i], max_index)):
            running_number_of_scratch_cards[j] += running_number_of_scratch_cards[i]
    return sum(running_number_of_scratch_cards)


def compute_part_one(file_name: str) -> int:
    cards = read_input_file(file_name)
    total_scratchcards_value = 0
    list_of_numbers = []
    for card in cards:
        number_of_winning_numbers = 0
        for winning_number in card.winning_numbers:
            if winning_number in card.my_numbers:
                number_of_winning_numbers += 1
        card_value = 0 if number_of_winning_numbers == 0 else 2 ** (number_of_winning_numbers - 1)
        list_of_numbers.append(number_of_winning_numbers)
        total_scratchcards_value += card_value

    return total_scratchcards_value, list_of_numbers


if __name__ == '__main__':
    total_scratchcards_value, list_of_numbers = compute_part_one('input/input4.txt')
    print(f"Part I: {total_scratchcards_value}")
    print(f"Part II: {compute_part_two(list_of_numbers)}")
