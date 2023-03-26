from gym_schafkopf.envs.player  import PlayerNN, PlayerRANDOM, PlayerHUMAN
from gym_schafkopf.envs.deck    import Deck
from gym_schafkopf.envs.helper  import sortCards, getPoints, getMoney, convertCards2Idx, createCardByIdx, createActionByIdx, convert2Idx

class Schafkopf():
    def __init__(self, options_dict):
        self.resetGame(options_dict)

    def resetGame(self, options_dict):
        # Independent stuff:
        self.options           = options_dict
        self.player_types      = options_dict["type"] # set here the player type
        self.player_names      = options_dict["names"]
        self.seed              = options_dict["seed"] # none for not using it
        self.print_            = options_dict["print_"]
        self.initialCard       = None  # the first card of a new round important for "bekennen"
        self.move              = 0
        self.current_round     = 0
        self.nu_games_played   = 0
        self.players           = []  # stores players object
        self.active_player     = options_dict["active_player"]  # due to gym reset =3 stores which player is active (has to give a card)
        self.gameOver          = 0
        # self.game_start_player = self.active_player
        # self.rewards           = np.zeros((self.nu_players,))
        # self.total_rewards     = np.zeros((self.nu_players,))

        # Table options:
        #self.decl_options   = ["weg", "ruf_E", "ruf_G", "ruf_S", "wenz", "geier", "solo_E", "solo_G", "solo_H", "solo_S"] # ordered declaration_options
        self.phase          = 0 # 0: declaration, 1: playing
        self.table          = [None, None, None, None]
        self.gameType       = "RAMSCH"

        # for save and storing a game:
        self.initialHandsIdx = []
        self.movesIdx        = []

        # only relevant for an MCTS Player
        self.saveTree          = 0
        if "save_tree" in options_dict:
            self.saveTree          = options_dict["save_tree"]

    def createDeck(self):
        d = Deck(seed=self.seed)
        d.shuffle()
        return d

    def createPlayer(self, name, type):
        if type=="RANDOM":
            return PlayerRANDOM(name, seed=self.seed)
        elif "MCTS" in type:  #"MCTS_10_50" is also a type option 10=subsamples, 50 = playouts
            from gym_schafkopf.envs.player  import PlayerMCTS
            return PlayerMCTS(name, self, type, seed=self.seed)
        elif type=="NN":
            return PlayerNN
        elif type=="HUMAN":
            return PlayerHUMAN
        else:
            print("ERROR Type not known!")
            return None

    # generate a Game:
    def setup_game(self):
        d = self.createDeck()
        for i in range(len(self.player_names)):
            p = self.createPlayer(self.player_names[i], self.player_types[i])
            p.draw(d, numCards=8)
            self.players.append(p)
            if self.print_:
                p.showHand()
            # used for replaying and storing a game!
            if self.move==0: self.initialHandsIdx.append(convertCards2Idx(p.hand))

    def evaluateTable(self):
        sortedCards = sortCards(self.table, gameType=self.gameType, initialCard=self.table[0])
        hightestCard = sortedCards[0]
        playerWithHighestCard = self.table.index(hightestCard)
        points       = getPoints([self.table])
        return hightestCard, playerWithHighestCard, points

    def getPlayerAction(self, cp, humanIdx=-1):
        if cp.type == "RANDOM":
            return cp.getAction(self.initialCard, self.phase, self.gameType)
        elif "MCTS" in cp.type:
             return cp.getAction(self.getGameState(), self.phase, print_=self.print_, saveTree=self.saveTree)
        # elif cp.type == "NN":
        #     return cp.getAction(self.getState())
        # elif cp.type == "HUMAN":
        #     return humanIdx
        # else:
        #     print("ERROR Player Name not valid!")

    def action2Idx(self, action):
        if type(action) == int and action<0:
            return -1 # not possible move
        if type(action) == str:
            if action == "weg":
                return 32
        else: # the action is a card:
            return action.idx

    def getNextPlayer(self):
        # remove this function is contained in helper
        if self.active_player == 3:
            return 0
        else:
            return self.active_player+1

    def getInitialCard(self):
        if self.table.count(None)==3:
            for i in self.table:
                if i is not None:
                    return i
        return self.initialCard # otherwise initialCard would be None!

    def finischGame(self):
        points = [p.points for p in self.players]
        money  = getMoney(points, gameType=self.gameType)
        for i,p in enumerate(self.players):
            p.money = money[i]
        if self.print_:
            for p in self.players:
                p.showResult()
        self.nu_games_played+=1
        self.gameOver = 1       
        return points, money

    # a game step
    def step(self, humanIdx=-1, customIdx=-1):
        # humanIdx not yet used / implemented TODO?!
        # customIdx is a valid action cardIndex 0...32
        cp        = self.players[self.active_player]
        if customIdx<0:
            action    = self.getPlayerAction(cp, humanIdx) # TODO FOR HUMANS
            actionIdx = self.action2Idx(action)
        else: # used in the replay case -> I do not have to calculate the action again its in the replay moves!
            actionIdx = customIdx
            action    = createActionByIdx(actionIdx)
            # remove the card from the hand!
            if self.phase == 1:
                cp.removeCardIdx(actionIdx)

        # if actionIdx negative -> action is not possible!
        if actionIdx<0:
            print("invalid Action")
            # TODO

        if self.phase == 0:
            cp.declaration = actionIdx # TODO <- remove this?!
            self.active_player = self.getNextPlayer()
            if self.move == 3:
                self.phase = 1
                #TODO get highest declaration here this player starts!
                self.gameType = "RAMSCH"
                self.active_player = 0
                if self.print_: print(str(self.current_round)+"-"+str(self.move)+": "+cp.name +" " +cp.type +" declares "+str(action)+"\n")
                self.current_round +=1
            else:
                if self.print_: print(str(self.current_round)+"-"+str(self.move)+": "+cp.name +" " +cp.type +" declares "+str(action))
        else:
            self.table[self.active_player] = action
            self.initialCard = self.getInitialCard()
            if (self.move+1)%4==0:
                # round ends
                hC, winnerIdx, points = self.evaluateTable()
                self.players[winnerIdx].update(points, hC, self.table)
                self.table = [None, None, None, None]
                self.initialCard = None
                self.active_player = winnerIdx
                if self.print_:
                    print(str(self.current_round)+"-"+str(self.move)+": "+cp.name +" " +cp.type +" plays "+str(action))
                    print("\tWinner: "+self.players[winnerIdx].name+ " with "+str(hC)+ " --> "+ str(points)+"\n")
                self.current_round +=1
            else:
                if self.print_: print(str(self.current_round)+"-"+str(self.move)+": "+cp.name +" " +cp.type +" plays "+str(action))
                self.active_player = self.getNextPlayer()
        self.move +=1
        self.movesIdx.append(actionIdx)
        if self.move == 36:
            points, money = self.finischGame()
            return True, points, money # game is finished!
        return False, None, None # game not finished!

 ### Functions used for MCTS Player
    def getGameState(self):
        actions = convert2Idx(self.players[self.active_player].getOptions(self.initialCard, phase = self.phase, gameType=self.gameType))
        gameState ={"options": self.options, "moves": self.movesIdx, "initialHandsIdx": self.initialHandsIdx, "activePlayer": self.active_player,
                    "gameOver": self.gameOver, "actions": actions}
        
        return gameState

    def replayGame(self,  moves=[], handCards=[]):
        # each repalyGame starts with an empty game:
        if self.print_: print("REPLAY GAME NOW: ", moves)
        self.resetGame(self.options)
        self.setup_customGame(handCards)
        for i in moves:
            self.step(customIdx=i)

    def setup_customGame(self, cardsIdx=[]):
        # used for replaying a game!
        for i in range(len(self.player_names)):
            p = self.createPlayer(self.player_names[i], self.player_types[i])
            playerCardsIdx = cardsIdx[i]
            p.hand = [createCardByIdx(i) for i in playerCardsIdx]
            self.players.append(p)
            if self.print_:
                p.showHand()
            # used for replaying and storing a game!
            if self.move==0: self.initialHandsIdx.append(convertCards2Idx(p.hand))