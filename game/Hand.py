from .Card import Card


class PokerHand:
    def __init__(self, hole_cards : list, board_cards : list):
        self.cards = hole_cards + board_cards
        if len(self.cards) < 5:
            raise ValueError("Not enough cards to evaluate a hand.")

    def evaluate(self):
        dups = self.max_duplicate_rank_count()
        s = self.has_straight()
        f = self.has_flush()
        if s and f:
            if self.has_straight_flush():
                return 8
        if dups[3] == 1:
            return 7
        if dups[2] >= 1 and (dups[1] + dups[2] >= 2):
            return 6
        if f:
            return 5
        if s:
            return 4
        if dups[2] == 1:
            return 3
        if dups[1] >= 2:
            return 2
        if dups[1] == 1:
            return 1
        return 0

    def has_flush(self):
        suit_counts = {}
        for card in self.cards:
            suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1
        return max(suit_counts.values()) >= 5

    def has_straight(self):
        values = sorted({card.get_value() for card in self.cards}, reverse=True)
        if 12 in values:
            values.append(-1)
        for i in range(len(values) - 4):
            window = values[i : i + 5]
            if all(window[j] - 1 == window[j + 1] for j in range(4)):
                return True
        return False

    def has_straight_flush(self):
        suit_groups = {s: [] for s in range(4)}
        for card in self.cards:
            suit_groups[card.suit].append(card.get_value())
        for values in suit_groups.values():
            values = sorted(set(values), reverse=True)
            if 12 in values:
                values.append(-1)
            for i in range(len(values) - 4):
                window = values[i : i + 5]
                if all(window[j] - 1 == window[j + 1] for j in range(4)):
                    return True
        return False

    def max_duplicate_rank_count(self):
        rank_counts = {}
        for card in self.cards:
            rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

        dupArr = [0, 0, 0, 0]
        for i in rank_counts.values():
            dupArr[i - 1] += 1

        return dupArr

    def get_kicker_values(self, n : int):
        if n in [0, 1, 2, 3, 6, 7]:
            rank_counts = {}
            for card in self.cards:
                val = card.get_value()
                rank_counts[val] = rank_counts.get(val, 0) + 1
            sorted_by_freq = sorted(
                rank_counts.items(), key=lambda x: (x[1], x[0]), reverse=True
            )
            return [val for val, count in sorted_by_freq]
        if n == 8:  # Straight flush
            suit_groups = {s: [] for s in range(4)}
            for card in self.cards:
                suit_groups[card.suit].append(card.get_value())

            for values in suit_groups.values():
                values = sorted(set(values), reverse=True)
                if 12 in values:
                    values.append(-1)
                for i in range(len(values) - 4):
                    window = values[i : i + 5]
                    if all(window[j] - 1 == window[j + 1] for j in range(4)):
                        return window
            raise ValueError("No straight flush present")
        if n == 5:
            suits = {0: [], 1: [], 2: [], 3: []}
            for card in self.cards:
                suits[card.suit].append(card)
            flush_suit = None
            for suit, cards in suits.items():
                if len(cards) >= 5:
                    flush_suit = suit
                    break
            if flush_suit is None:
                raise ValueError("No flush present")
            flush_cards = sorted(
                suits[flush_suit], key=lambda c: c.get_value(), reverse=True
            )
            return [card.get_value() for card in flush_cards[:5]]
        if n == 4:
            values = sorted({card.get_value() for card in self.cards}, reverse=True)
            if 12 in values:
                values.append(-1)
            for i in range(len(values) - 4):
                window = values[i : i + 5]
                if all(window[j] - 1 == window[j + 1] for j in range(4)):
                    return window
            raise ValueError("No straight present")

    def randBoard():
        used_cards = set()

        def deal_unique_card():
            while True:
                card = Card.random_card()
                if card not in used_cards:
                    used_cards.add(card)
                    return card

        return PokerHand(
            [deal_unique_card(), deal_unique_card()],
            [
                deal_unique_card(),
                deal_unique_card(),
                deal_unique_card(),
                deal_unique_card(),
                deal_unique_card(),
            ],
        )

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)

