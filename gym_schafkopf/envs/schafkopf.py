lass game(metaclass=abc.ABCMeta):
    def __init__(self, options_dict):
        # Independent stuff:
        self.player_types      = options_dict["type"] # set here the player type RANDOM or RL (reinforcement player)
        self.player_names      = options_dict["names"]
        self.nu_cards          = options_dict["nu_cards"] #         #Number of cards e.g. 15(maximum), or 4 -> 12,13,14,15 of each color is given.
        self.seed              = options_dict["seed"] # none for not using it
        self.nu_players        = len(self.player_names)
        self.current_round     = 0
        self.nu_games_played   = 0
        self.players           = []  # stores players object
        self.on_table_cards    = []  # stores card on the table
        self.active_player     = options_dict["active_player"]  # due to gym reset =3 stores which player is active (has to give a card)
        self.played_cards      = []  # of one game # see also in players offhand!
        self.gameOver          = 0
        self.game_start_player = self.active_player
        self.rewards           = np.zeros((self.nu_players,))
        self.total_rewards     = np.zeros((self.nu_players,))
        self.colors            = options_dict["colors"]
        self.value_conversion  = options_dict["value_conversion"]
#### independent
#### independent functions
#### independent

    def createDeck(self):
        myDeck = deck(self.nu_cards, self.colors, self.value_conversion, self.seed)
        myDeck.shuffle()
        return myDeck

    def hand2Cards(self, playeridx, cards):
        return [self.players[playeridx].hand[i] for i in cards]

    def idx2Card(self, idx):
        # input unique card index output: card object
        myDeck = deck(self.nu_cards, self.colors, self.value_conversion, self.seed)
        for card in myDeck.cards:
            if card.idx == idx:
                return card

    def idxOfName(self, cardValue, cardColor):
        cards = deck(self.nu_cards, self.colors, self.value_conversion, self.seed).cards
        card = self.getSpecificCard(cardValue, cardColor, [cards], doConversion=True)
        if card is not None:
            return card.idx
        return None

    def idx2Hand(self, idx, player_idx):
        #returns hand index of unique idx
        for i, card in enumerate(self.players[player_idx].hand):
            if card.idx == idx:
                return i
        return None

    def idxList2Cards(self, idxlist):
        result  = []
        for j in idxlist:
            result.append(self.idx2Card(j))
        return result

    # generate a Game:
    def setup_game(self):
        myDeck = self.createDeck()
        self.total_rounds      = int(len(myDeck.cards)/self.nu_players)
        for i in range (self.nu_players):
            play = player(self.player_names[i], self.player_types[i], colors = self.colors)
            play.draw(myDeck, self.total_rounds)
            play.hand = play.getHandCardsSorted()
            self.players.append(play)

        # print("Show HANDDD")
        # for p in self.players:
        #     p.showHand()
    def card2Idx(self, suit, rank):
        test = deck(self.nu_cards, self.colors, self.value_conversion, self.seed)
        for i in test.cards:
            if i.color == suit and int(i.value)==int(rank):
                return i.idx
        return -1

    def state2Cards(self, state_in):
        #in comes a state matrix with len = 60 with 0...1..0...1
        indices = [i for i, x in enumerate(state_in) if int(x) == 1]
        result  = []
        for j in indices:
            result.append(self.idx2Card(j))
        return result

    def splitState(self, state=None):
        if state is None:
            state = self.getState().flatten().astype(int)
        else:
            state = state.flatten().astype(int)
        ll    = self.nu_players * self.nu_cards
        #[on_table+ on_hand+ played+ play_options+ add_states+matching+decl_options+[self.active_player]]
        on_table, on_hand, played, play_options= state[0:ll], state[ll:2*ll], state[ll*2:3*ll], state[3*ll:4*ll]
        add_states, matching, decl_opts, cp = state[4*ll:4*ll+18], state[4*ll+18:len(state)-(1+len(self.decl_options))], state[len(state)-(1+len(self.decl_options)):len(state)-1], state[len(state)-1]
        return on_table, on_hand, played, play_options, add_states, matching, decl_opts, cp

    def getPartners(self, active_player, matchingBinary):
        matchingBinary[active_player] = 10
        result = ""
        for i in matchingBinary:
            if int(i)==1:
                result+=self.player_names[i]
        return result

    def printCurrentState(self, state=None):
        #Note: ontable, onhand played play_options laenge = players* cards
        on_table, on_hand, played, play_options, add_states, matching, decl_opts, cp = self.splitState(state)
        print("State for", self.player_names[cp])
        for i,j in zip([on_table, on_hand, played, play_options], ["on_table", "on_hand", "played", "options"]):
             #print(j, i, self.state2Cards(i))
             print("\t", j, len(i),self.state2Cards(i))

        # print the matching
        print("\t", "partners:", self.player_names[cp]+"_"+str(cp)+"(you) play with "+self.getPartners(cp, matching))
        enemy_tmp = [0,1,2,3]
        enemy_tmp.remove(cp)
        splited_list = np.array_split(add_states,3)
        for j,play_list in enumerate(splited_list):
            print("\t","Add_state for ", self.player_names[enemy_tmp[j]])
            print("\t \t"," would_win", play_list[0], "is free of trump", play_list[5], "color(EGHZ) free", play_list[1:5])
        decl_names = []
        for j, i in enumerate(decl_opts):
            if i==1:
                decl_names.append(self.convertIndex2Decl(j+32))
        print("\t","Declaration options", decl_names, decl_opts)

    def nextGamePlayer(self):
        if self.game_start_player < self.nu_players-1:
            self.game_start_player+=1
        else:
            self.game_start_player = 0
        return self.game_start_player

    def getPreviousPlayer(self, input_number):
        if input_number == 0:
            prev_player = self.nu_players-1
        else:
            prev_player = input_number -1
        return prev_player

    def getNextPlayerIdx(self, input_number):
        next_player = input_number
        if input_number < self.nu_players-1:
            next_player +=1
        else:
            next_player = 0
        return next_player

    def getNextPlayer(self):
        # manipulates active player
        # delete this function and use only below one! (TODO)
        if self.active_player < self.nu_players-1:
            self.active_player+=1
        else:
            self.active_player = 0
        return self.active_player

    def getNextPlayer_(self):
        # does not manipulate the active player!
        tmp = self.active_player
        if tmp < self.nu_players-1:
            tmp+=1
        else:
            tmp = 0
        return tmp

    def getRandomCard(self):
        return random.randrange(len(self.players[self.active_player].hand))

    def getRandomValidOption(self):
        # return an index of a card or a declaration index
        cp = self.active_player
        if self.phase == "declaration":
            # find random index in allowed_decl=[1.0, 1.0, 1.0, 1.0] that is 1.0
            allowed_decl = self.getBinaryDeclarations(cp)
            rand_idx     = random.randrange(0, int(sum(allowed_decl)))
            tmp          = 0
            for j, i in enumerate(allowed_decl):
                if tmp == rand_idx:
                    break
                if int(i) == 1:
                    tmp +=1
            return j+self.nu_players*self.nu_cards
        elif self.phase == "playing":
            valid_options_as_cards = self.getValidOptions(self.on_table_cards, self.active_player)# cards
            rand_idx               = random.randrange(len(valid_options_as_cards))
            card                   = valid_options_as_cards[rand_idx]
            return card.idx

    def getRandomOption_(self):
        incolor = None
        if len(self.on_table_cards)>0:
            incolor = self.on_table_cards[0].color
        options = self.getOptions(incolor, self.players[self.active_player].hand)#hand index
        if len(options) == 0:
            print("Error has no options left!", options, self.players[self.active_player].hand)
            return None
        rand_card = random.randrange(len(options))
        return rand_card

    def isGameFinished(self):
        cards = 0
        for player in self.players:
            cards += len(player.hand)
        if cards == 0:
            return True
        else:
            return False

    def printHands(self):
        for i in range(len(self.players)):
            print(self.player_names[i]+" ["+self.player_types[i]+"] ", self.players[i].hand)

    def hasSpecificCard(self, cardValue, cardColor, cards, doConversion=False):
        for stich in cards:
            for card in stich:
                if card is not None:
                    if doConversion:
                        convValue = str(card.getConversion())
                    else:
                        convValue = card.value
                    if card.color == cardColor and convValue == cardValue:
                        return True
        return False

    def getSpecificCard(self, cardValue, cardColor, cards, doConversion=False):
        for stich in cards:
            for card in stich:
                if card is not None:
                    if doConversion:
                        convValue = str(card.getConversion())
                    else:
                        convValue = card.value
                    if card.color == cardColor and convValue == cardValue:
                        return card
        return None

    def cards2Idx(self, cardlist):
        result = []
        for i in cardlist:
            result.append(i.idx)
        return result
#### specific
#### specific functions every ard game should have
#### specific

    @abc.abstractmethod
    def reset(self):
        '''
        create and shuffle new deck
        reset game obj. parameters
        @return:   None
        '''
        pass

    @abc.abstractmethod
    def play_ai_move(self, ai_card_idx, print_=False):
        '''
        card idx from 0....

        @return:   None
        '''
        pass

    @abc.abstractmethod
    def playUntilAI(self, print_=False):
        '''
        @return:   rewards True True
        '''
        pass


    @abc.abstractmethod
    def stepRandomPlay(self, action_ai, print_=False):
        '''
        @return:   rewards True True
        '''
        pass

    @abc.abstractmethod
    def getInColor(self):
        '''
        @return:   None
        '''
        pass

    @abc.abstractmethod
    def evaluateWinner(self):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def getState(self):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def getValidOptions(self, player):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def convertTakeHand(self, player, take_hand):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def step(self, card_idx, print_=False):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def getAdditionalState(self, playeridx):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def getmyState(self, playeridx, players, cards):
        '''
        @return:
        '''
        pass

##### TODO - moved from player .....
### move below into witches class!
    @abc.abstractmethod
    def getOptions(self, incolor, orderOptions=False):
        '''
        @return:
        '''
        pass


    @abc.abstractmethod
    def countResult(self, input_cards, offhandCards):
        '''
        @return:
        '''
        pass

    @abc.abstractmethod
    def assignRewards(self):
        '''
        @return:
        '''
        pass
    @abc.abstractmethod
    def getBinaryOptions(self, incolor, players, cards, shifting):
        '''
        @return:
        '''
        pass
