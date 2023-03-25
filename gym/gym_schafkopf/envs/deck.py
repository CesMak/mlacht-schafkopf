import random
from gym_schafkopf.envs.card import Card
class Deck(object):
    def __init__(self, suits = ["E", "G", "H", "S"], ranks = ["7", "8", "9", "X", "U", "O", "K", "A"], seed=None):
        self.cards    = []
        self.nu_cards = len(suits)*len(ranks)
        self.suits    = suits
        self.ranks    = ranks
        if seed is not None:
            random.seed(seed)
        self.build()

    # Display all cards in the deck
    def show(self, oneline=True):
        res = ""
        for card in self.cards:
            if oneline:
                res +=card.show()+", "
            else:
                print(card.show())
        if oneline:
            print(res)
        return res

    def build(self):
        self.cards = []
        idx        = 0
        for suit in self.suits:
            for rank in  self.ranks:
                self.cards.append(Card(suit, rank, idx))
                idx +=1

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()