class Card(object):
    def __init__(self, suit: str, rank: str, idx: int):
        self.suit = suit # E G H S
        self.rank = rank # 7 8 9 10 U O K A
        self.idx  = idx

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
    def show_simple(self):
        return str("{}{}_{}".format(self.suit, self.rank, self.idx))
    def getName(self):
        return str(self.suit)+str(self.rank)
    def show(self):
        tmp = self.suit+""+self.rank
        if self.suit == "E":
            tmp = "\033[1;33m"+tmp
        elif self.suit == "G":
            tmp = "\033[1;32m"+tmp
        elif self.suit == "H":
            tmp = "\033[1;31m"+tmp
        else:
            tmp =  "\033[0;36m"+tmp# Schell is blue here!
        return tmp+"\033[0m"