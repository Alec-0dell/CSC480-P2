from itertools import combinations
from game.Card import Card
from game.State import PokerState
import time
import math


class MCTSNode:
    def __init__(self, hand: list):
        self.hand = hand
        self.visits = 0
        self.wins = 0

    def __str__(self) -> str:
        hand_str = f"[{self.hand[0]}, {self.hand[1]}]"
        return f"{hand_str}, visits: {self.visits}, wins: {self.wins}, win_rate: {self.win_rate():.2f}"

    def win_rate(self):
        return self.wins / self.visits if self.visits > 0 else 0


def simulate(state: PokerState, node):
    node.visits += 1
    sim = PokerState(list(state.mine), node.hand, list(state.board))
    sim.dealComplete()
    if sim.win() == 1:
        node.wins += 1


def makeDecisions(state):
    start_time = time.time()
    time_limit = 10
    n = set()
    for rank in range(1, 14):
        for suit in range(4):
            c = Card(rank, suit)
            if c not in set(state.mine + state.board):
                n.add(c)
    nodes = [MCTSNode(list(hand)) for hand in combinations(n, 2)]
    sims = 0
    for node in nodes:
        sims += 1
        simulate(state, node)

    while time.time() - start_time < time_limit:
        if sims % 15000 == 0:
            print("Working...")
        maxUCB = 0
        maxNode = None
        for i in nodes:
            ucb = i.wins / i.visits + math.sqrt(2) * math.sqrt(
                math.log(sims) / i.visits
            )
            if maxUCB < ucb:
                maxUCB = ucb
                maxNode = i
        sims += 1
        simulate(state, maxNode)
    
    wins = 0
    # maxwr = 0
    # minwr = 1
    # maxwh = None
    # minwh = None
    for i in nodes:
        wr = i.win_rate()
        # if wr > maxwr:
        #     maxwh = i
        #     maxwr = wr
        # if wr < minwr:
        #     minwh = i
        #     minwr = wr
        wins += wr
        
    wins = wins / len(nodes)

    print("Total sims:", sims)
    print("Win %:", wins)
    result = ""
    if wins >= 0.5:
        result = "Stay"
    else:
        result = "Fold"
        
    print("+--------+\n| ", result, " |\n+--------+")
    # print("Worst opposing hand:")
    # print(maxwh)
    # print("Best opposing hand:")
    # print(minwh)
