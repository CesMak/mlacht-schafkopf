from gym_schafkopf.envs.helper  import sortCards, getTrumps, getSuits, getCardOrder, createActionByIdx, convertIdx2CardMCTS, convertCards2Idx, subSamplev2
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
        return self.hand

    def setColorFree(self, color):
        for j, i in enumerate(["E","G","H","S"]):
            if color == i:
                self.suitFree[j+1] = 1.0

    def setTrumpFree(self):
        self.suitFree[0] = 1.0

    def removeCardIdx(self, idx):
        # e.g. idx = 0 -> remove E7 from hand
        cardsIdx = convertCards2Idx(self.hand)
        self.hand.pop(cardsIdx.index(idx))

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
    # Player that plays random action
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
class PlayerHUMAN(Player):
    # Player that is used for replay game?!
    def __init__(self, name):
        super().__init__(name, type="HUMAN")
    def getAction(possibleCards:list):
        print("TODO")

from gym_schafkopf.envs.mcts.mct  import MonteCarloTree
class PlayerMCTS(Player):
    def __init__(self, name, schafObj, type, seed = None):
        super().__init__(name, type="MCTS")
        if seed is not None: random.seed(seed)
        self.schafObj = schafObj
        # default values:
        self.num_subSamples = 10 # how often should the players be subsampled
        self.num_playouts   = 50 # how often do you do the mcts kind of depth
        self.ucb_const      = 50 # mcts const of selecting the best child
        # type: MCTS_SUBSAMPLES_PLAYOUTS_UCBCONST
        #       MCTS_OFF_50 -> use real handCards (do not subsample at all)
        if "_" in type:
            tmp = type.split("_")
            if len(tmp)>1:
                if "OFF" in str(tmp[1]):
                    self.num_subSamples = -1
                else:
                    self.num_subSamples = int(tmp[1])
            if len(tmp)>2:
                self.num_playouts   = int(tmp[2])
            if len(tmp)>3:
                self.ucb_const      = int(tmp[3])
    def getAction(self, gS, phase, print_=False):
        actionsIdx = gS["actions"]
        if len(actionsIdx) > 1:
            oba = {}
            if self.num_subSamples<0: # OFF use real hand Cards!
                mct =  MonteCarloTree(gS, self.schafObj, ucb_const=self.ucb_const)
                oba = mct.uct_search(self.num_playouts, print_=False)
            else:  # do subsample required for simulating real games!
                for _ in range(self.num_subSamples):
                    gS["initialHandsIdx"] =  subSamplev2(gS["moves"], gS["activePlayer"], self.hand)
                    mct =  MonteCarloTree(gS, self.schafObj, ucb_const=1)
                    mcts_action = mct.uct_search(self.num_playouts, print_=False)
                    ba = max(mcts_action, key=mcts_action.get)
                    if print_: print("SAMPLE actions and visits:", mcts_action, convertIdx2CardMCTS(mcts_action), "best action->", ba, createActionByIdx(ba))
                    if ba not in oba:
                        oba[ba] = 1
                    else:
                        oba[ba]+=1
            best_action=max(oba, key=oba.get) 
            if print_: print("TOTAL: best action: ", createActionByIdx(best_action), oba)

        else:
            best_action = actionsIdx[0] # if there is only one option return it!
        if phase == 1:
            self.removeCardIdx(best_action)
        return createActionByIdx(best_action)
