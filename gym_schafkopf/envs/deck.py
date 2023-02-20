class deck(object):
    def __init__(self, nu_cards, colors=['B', 'G', 'R', 'Y'], value_conversion={}, seed=None):
        self.cards    = []
        self.nu_cards = nu_cards
        self.colors   = colors
        self.value_conversion= value_conversion
        if seed is not None:
            random.seed(seed)
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print(card.show())

    # Green Yellow Blue Red
    def build(self):
        self.cards = []
        idx        = 0
        for color in self.colors:
            for val in range(1, self.nu_cards+1):# choose different deck size here! max is 16
                self.cards.append(card(color, val, idx, value_conversion = self.value_conversion))
                idx +=1

    # Shuffle the deck
    def shuffle(self, num=1):
        random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()