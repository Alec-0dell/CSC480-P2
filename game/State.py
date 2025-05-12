import random
from .Hand import PokerHand
from .Card import Card


class PokerState:
    def __init__(self, mine: list, yours: list, board: list):
        if len(mine) not in [0, 2]:
            raise ValueError("You must have exactly 2 cards in your hand.")
        if len(yours) not in [0, 2]:
            raise ValueError("Opponent must have exactly 2 cards in their hand.")
        if len(board) not in [0, 3, 4, 5]:
            raise ValueError("Board must have 0, 3, 4, or 5 cards.")

        self.mine = mine
        self.yours = yours
        self.board = board
        self.complete = len(board) == 5

    def __str__(self):
        mine_str = ", ".join(str(card) for card in self.mine)
        yours_str = ", ".join(str(card) for card in self.yours)
        board_str = ", ".join(str(card) for card in self.board)
        return (
            f"My Hand:      {mine_str}\n"
            f"Board:        {board_str if self.board else 'No cards'}\n"
            f"Opponent Hand:{yours_str}"
        )

    def gamestr(self):
        mine_str = ", ".join(str(card) for card in self.mine)
        board_str = ", ".join(str(card) for card in self.board)
        return (
            f"My Hand:      {mine_str}\n"
            f"Board:        {board_str if self.board else 'No cards'}"
        )

    def win(self):
        if not self.complete:
            raise ValueError("Cannot evaluate winner: the board must have 5 cards.")

        my_hand = PokerHand(self.mine, self.board)
        their_hand = PokerHand(self.yours, self.board)

        my_score = my_hand.evaluate()
        their_score = their_hand.evaluate()

        if my_score == their_score:
            my_kickers = my_hand.get_kicker_values(my_score)
            their_kickers = their_hand.get_kicker_values(my_score)
            if my_kickers > their_kickers:
                return 1
            elif their_kickers > my_kickers:
                return -1
            else:
                return 0
        if my_score > their_score:
            return 1
        else:
            return -1

    @staticmethod
    def randGame():
        cards = set()
        while len(cards) < 9:
            cards.add(Card.random_card())
        cards = list(cards)
        random.shuffle(cards)
        mine = [cards.pop(), cards.pop()]
        yours = [cards.pop(), cards.pop()]
        board = [cards.pop() for _ in range(5)]
        return PokerState(mine, yours, board)

    def deal(self):
        if self.complete:
            return
        used_cards = set(self.mine + self.yours + self.board)

        def deal_unique_card():
            while True:
                card = Card.random_card()
                if card not in used_cards:
                    used_cards.add(card)
                    return card

        if len(self.mine) == 0 or len(self.yours) == 0:
            self.mine = [deal_unique_card(), deal_unique_card()]
            self.yours = [deal_unique_card(), deal_unique_card()]
            return
        if len(self.board) == 0:
            self.board.extend([deal_unique_card() for _ in range(3)])
        elif len(self.board) == 3:
            self.board.append(deal_unique_card())
        elif len(self.board) == 4:
            self.board.append(deal_unique_card())
        self.complete = len(self.board) == 5

    def dealComplete(self):
        if self.complete:
            return
        used_cards = set(self.mine + self.yours + self.board)

        def deal_unique_card():
            while True:
                card = Card.random_card()
                if card not in used_cards:
                    used_cards.add(card)
                    return card

        if len(self.board) == 0:
            self.board.extend([deal_unique_card() for _ in range(5)])
        elif len(self.board) == 3:
            self.board.extend([deal_unique_card() for _ in range(2)])
        elif len(self.board) == 4:
            self.board.append(deal_unique_card())
        self.complete = True
        return self
