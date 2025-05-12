import random
from game.Card import Card
from game.Hand import PokerHand
from game.State import PokerState
from PokerBot import makeDecisions



if __name__ == "__main__":
    s = PokerState([], [], [])
    
    input("Press Enter to deal hole cards (Pre-Flop)...")
    s.deal()
    print(s.gamestr())
    makeDecisions(s)

    input("Press Enter to deal the Flop...")
    s.deal()
    print(s.gamestr())
    makeDecisions(s)

    input("Press Enter to deal the Turn...")
    s.deal()
    print(s.gamestr())
    makeDecisions(s)

    input("Press Enter to deal the River...")
    s.deal()
    print(s.gamestr())
    makeDecisions(s)
    
    input("Press Enter to reveal results...")
    w = s.win()
    if w == 1:
        print("+----------+\n| You WON! |\n+----------+")
    elif w == -1:
        print("+-------------+\n| You lost... |\n+-------------+")
    elif w == 0:
        print("+-------------+\n| It's a tie. |\n+-------------+")
    print(s)