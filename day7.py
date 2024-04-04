import re
from collections import Counter
from dataclasses import dataclass, field
from operator import itemgetter

# regular card order (part I of the puzzle)
card_order = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7,
              "6": 6, "5": 5, "4": 4, "3": 3, "2": 2}
# in case of a Joker J, the value of J will be 1 (part II of the puzzle)


@dataclass
class Hand:
    cards: str
    bid: int
    type: int = 1

    def __post_init__(self):
        card_count = {i: self.cards.count(i) for i in self.cards}
        card_count_sorted = dict(sorted(card_count.items(), key=itemgetter(1), reverse=True))
        card_count_sorted_values = list(card_count_sorted.values())

        # alternative is using the Counter function
        # card_count_sorted_values = list(sorted(Counter(hand.cards).values(), reverse=True))

        if card_count_sorted_values[0] == 5:
            self.type = 7  # five of a kind
        elif card_count_sorted_values[0] == 4:
            self.type = 6  # four of a kind
        elif card_count_sorted_values[0] == 3 and card_count_sorted_values[1] == 2:
            self.type = 5  # full house
        elif card_count_sorted_values[0] == 3:
            self.type = 4  # three of a kind
        elif card_count_sorted_values[0] == card_count_sorted_values[1] == 2:
            self.type = 3  # two pair
        elif card_count_sorted_values[0] == 2:
            self.type = 2  # one pair
        else:
            self.type = 1  # high card


def read_input_file(file_name: str) -> list:
    hands = []
    with open(file_name) as f:
        content = f.read().splitlines()
    for line in content:
        card, bid = line.split()
        hand = Hand(card, int(bid))
        hands.append(hand)

    return hands


def joker_evaluation(hand: Hand) -> None:
    """evaluates Joker hands
    """

    number_of_jacks = Counter(hand.cards)["J"]
    if "J" not in hand.cards:
        return
    else:
        if hand.type == 6 or hand.type == 5:
            # 4 of a kind of full house -> five of a kind
            hand.type = 7
            return
        if hand.type == 4:
            # three of a kind -> four of a kind
            hand.type = 6
            return
        if hand.type == 3 and number_of_jacks == 2:
            # two pair -> four of a kind
            hand.type = 6
            return
        if hand.type == 3 and number_of_jacks == 1:
            # two pair -> three of a kind
            hand.type = 5
            return

        if hand.type == 2:
            # one pair -> three of a kind
            hand.type = 4
            return
        if hand.type == 1:
            # high card -> one pair
            hand.type = 2
            return

    return


def sort_hands(hand_types: list) -> list:
    """"sort the hands based first on hand-type and then on card-order 0-4"""
    hand_types_sorted = sorted(hand_types, key=lambda x: (x[1], card_order[x[0].cards[0]],
                                                          card_order[x[0].cards[1]],
                                                          card_order[x[0].cards[2]],
                                                          card_order[x[0].cards[3]],
                                                          card_order[x[0].cards[4]]))

    return hand_types_sorted


def compute_part_one(file_name: str) -> int:
    hands = read_input_file(file_name)
    hand_types = []
    for hand in hands:
        # hand_type = hand_evaluation(hand)
        # hand_types.append([hand, hand_type])
        hand_types.append([hand, hand.type])

    sorted_hand_types = sort_hands(hand_types)
    total_winnings = 0
    for i, ht in enumerate(sorted_hand_types, start=1):
        total_winnings += i * ht[0].bid

    return total_winnings


def compute_part_two(file_name: str) -> int:
    hands = read_input_file(file_name)

    for hand in hands:
        joker_evaluation(hand)
    card_order["J"] = 1  # Joker will be the lowest card in the deck

    hand_types = []
    for hand in hands:
        hand_types.append([hand, hand.type])

    sorted_hand_types = sort_hands(hand_types)
    total_winnings = 0
    for i, ht in enumerate(sorted_hand_types, start=1):
        total_winnings += i * ht[0].bid

    return total_winnings


if __name__ == '__main__':
    print(f"Part I: {compute_part_one('input/input7.txt')}")
    print(f"Part II: {compute_part_two('input/input7.txt')}")
