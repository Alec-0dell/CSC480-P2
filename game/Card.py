import random

class Card:
    SUITS = ["♥️", "♦️", "♣️", "♠️"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    RANK_VALUES = {r: i for i, r in enumerate(RANKS)}

    def __init__(self, rank : int , suit : int):
        if not (1 <= rank <= 13):
            raise ValueError(f"Invalid rank: {rank}")
        if not (0 <= suit <= 3):
            raise ValueError(f"Invalid suit: {suit}")
        self.rank = rank  # 1=Ace, 13=King
        self.suit = suit  # 0-3

    def rank_str(self):
        return Card.RANKS[self.rank - 2 if self.rank != 1 else 12]

    def suit_str(self):
        return Card.SUITS[self.suit]

    def __str__(self):
        return f"{self.rank_str()}{self.suit_str()}"

    def __lt__(self, other):
        return self.get_value() < other.get_value()

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def get_value(self):
        return 12 if self.rank == 1 else self.rank - 2

    def random_card():
        rank = random.randint(1, 13)
        suit = random.randint(0, 3)
        return Card(rank, suit)