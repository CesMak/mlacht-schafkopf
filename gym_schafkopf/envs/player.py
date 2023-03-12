from gym_schafkopf.envs.helper  import sortCards, getTrumps, getSuits, getCardOrder
class Player(object):
    def __init__(self, name, type):
        self.name         = name        # players name
        self.type         = type        # type e.g. RANDOM, HUMAN, NN=Neuronal Network, MCTS=MONTE CARLO TREE SEARCH
        self.declaration  = ""          # weg
        self.points       = 0           # 0...120 depending on the tricks he made
        self.money        = 0           # depending on the gametype and points money is calculated
        self.hand         = []          # cards one player has on its hand after dealing
        self.offhand      = []          # contains won cards of each round (for 4 players 4 cards!) = tricks
        self.suitFree     = [0.0, 0.0, 0.0, 0.0, 0.0]# trump free, color free <- used as gameState in the NN
        # members for sorting cards:
        self.handSorted   = False

    def sayHello(self):
        print ("Hi! My name is {}.".format(self.name))
        return self

    # Draw n number of cards from a deck
    # Returns true if n cards are drawn, false if less then that
    def draw(self, deck, numCards=1):
        for _ in range(numCards):
            card = deck.deal()
            if card:
                card.player = self.name
                self.hand.append(card)
            else:
                return False
        return True

    # Display all the cards in the players hand
    def showHand(self):
        print ("{}'s hand: {} type: {}".format(self.name, self.getHandCardsSorted(), self.type))
        return self

    def showResult(self):
        print ("{}'s hand: {} offhand: {} points: {} --> {}$".format(self.name, self.getHandCardsSorted(), str(self.offhand), self.points, self.money))

    def update(self, points, cardToDiscard, trick):
        self.points += points
        self.offhand.append(trick)

    def getHandCardsSorted(self, gameType="RAMSCH"):
        self.hand = sortCards(self.hand, gameType=gameType)
        self.handSorted   = True

    def setColorFree(self, color):
        for j, i in enumerate(["E","G","H","S"]):
            if color == i:
                self.suitFree[j+1] = 1.0

    def setTrumpFree(self):
        self.suitFree[0] = 1.0

    def getDeclarationOptions(self):
        # TODO check allowed declarations
        # TODO check hand cars EA, GA, SA if RUF is allowed or not etc.
        return ["weg"]

    def getPlayingOptions(self, initialCard, gameType="RAMSCH"):
        # Ramsch: Herz=Trumpf
        if not self.handSorted:
            self.getHandCardsSorted(gameType)
        if initialCard == None:
            # you are the first player
            return self.hand
        else:
            trumpIdx, _ = getCardOrder(gameType)
            if initialCard.idx in trumpIdx: # first card is a trump
                trumps = getTrumps(self.hand, gameType)
                if len(trumps)>0:
                    return trumps
                else: # if a trump is played but you do not have a trump!
                    self.setTrumpFree()
                    return self.hand
            else:
                suits = getSuits(self.hand, initialCard.suit, gameType)
                if len(suits)>0:
                    return suits
                else: # if a trump is played but you do not have a trump!
                    self.setColorFree(initialCard.suit)
                    return self.hand

    def getOptions(self, initialCard, phase=0, gameType="RAMSCH"):
        # get all possible Options for the player
        if phase == 0: # declaration
            return self.getDeclarationOptions()
        else:               # playing phase
            return self.getPlayingOptions(initialCard, gameType=gameType)

import random
class PlayerRANDOM(Player):
    def __init__(self, name, seed=None):
        super().__init__(name, type="RANDOM")
        if seed is not None: random.seed(seed)

    def getAction(self, initialCard, phase, gameType):
        opts=super().getOptions(initialCard, phase=phase, gameType=gameType)
        action =  opts[random.randrange(len(opts))]
        if phase == 1:
            self.hand.pop(self.hand.index(action)) # disard selected option!
        return action
class PlayerNN(Player):
    def __init__(self, name):
        super().__init__(name, type="NN")
    def getAction(state:list):
        print("TODO")

#from mcts.mct import MonteCarloTree
class PlayerMCTS(Player):
    def __init__(self, name):
        super().__init__(name, type="MCTS")
    def getAction(possibleCards:list):
        print("TODO")

class PlayerHUMAN(Player):
    def __init__(self, name):
        super().__init__(name, type="HUMAN")
    def getAction(possibleCards:list):
        print("TODO")