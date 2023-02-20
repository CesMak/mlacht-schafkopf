class player(object):
    def __init__(self, name, type, colors=['B', 'G', 'R', 'Y']):
        # how many different colors has the game
        # schafkopf, doppelkopf, witches, uno = 4
        self.name         = name
        self.hand         = []
        self.offhand      = [] # contains won cards of each round (for 4 players 4 cards!) = tricks
        self.take_hand    = [] # cards in first phase cards to take! used in witches, schafkopf hochzeit
        self.colorFree    = [0.0]*len(colors) # must be double for pytorch learning! 1.0 means other know that your are free of this color B G R Y
        self.trumpFree    = 0.0
        self.type         = type # HUMAN, RL=Automatic Bot, TODO change
        self.colors       = colors

    def sayHello(self):
        print ("Hi! My name is {}".format(self.name))
        return self

    # Draw n number of cards from a deck
    # Returns true if n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                card.player = self.name
                self.hand.append(card)
            else:
                return False
        return True

    # Display all the cards in the players hand
    def showHand(self):
        print ("{}'s hand: {}".format(self.name, self.getHandCardsSorted()))
        return self

    def discard(self):
        # returns most upper card and removes it from the hand!
        return self.hand.pop()

    def getHandCardsSorted(self):
        # this is used for showing the hand card nicely when playing
        return sorted(self.hand, key = lambda x: ( x.color,  x.value))

    def appendCards(self, stich):
        # add cards to the offhand.
        self.offhand.append(stich)

    def setColorFree(self, color):
        for j, i in enumerate(self.colors):
            if color == i:
                self.colorFree[j] = 1.0

    def setTrumpFree(self):
        self.trumpFree = 1.0

    def playRandomCard(self, incolor, options):
        if len(options) == 0:
            print("Error has no options left!", options, self.hand)
            return None
        rand_card = random.randrange(len(options))
        card_idx = 0
        card_idx  = options[rand_card][0]
        return self.hand.pop(card_idx)

    def hasSpecificCardOnHand(self, idx):
        # return True if the hand has this card!
        for i in self.hand:
            if i.idx == idx:
                return True
        return False