class card(object):
    def __init__(self, suit: str, rank: str, idx: int):
        if self.validate(suit, rank):
            self.suit = suit # E G H S
            self.rank = rank # 7 8 9 10 U O K A
            self.idx  = idx # 0...32  # each card has a unique index.
            return True 
        return False 

    def validate(self, suit: str, rank: str):
        if suit in ["E", "G", "H", "S"] and rank in ["7", "8", "9", "10", "U", "O", "K", "A"]:
            return True 
        return False

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
    def show(self):
        return str("u\"{}{}\"".format(self.suit, self.rank, self.idx))
    def show_colored(self):
        # TODO 
        # BRed='\033[1;31m'         # Red
        # BGreen='\033[1;32m'       # Green
        # BYellow='\033[1;33m'      # Yellow
        return "\033[91mThis is red text\033[0m"