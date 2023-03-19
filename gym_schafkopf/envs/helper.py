from gym_schafkopf.envs.card import Card

SORTEDCARDS = ["E7","E8","E9","EX","EU","EO","EK","EA","G7","G8","G9","GX","GU","GO","GK","GA","H7","H8","H9","HX","HU","HO","HK","HA","S7","S8","S9","SX","SU","SO","SK","SA"]

import random
def getCardOrder(gameType):
    trumpIdx  = [5, 13, 21, 29, 4, 12, 20, 28] +  [23, 19, 22, 18, 17, 16] 
    otherIdx  = [7, 3, 6, 2, 1, 0] + [15, 11, 14, 10, 9, 8] + [31, 27, 30, 26, 25, 24]
    if gameType=="RAMSCH" or "Ruf" in gameType:            
                    #eo                        SU      HA  H1  HK  H9  H8  H7
        trumpIdx  = [5, 13, 21, 29, 4, 12, 20, 28] +  [23, 19, 22, 18, 17, 16] 
        otherIdx  = [7, 3, 6, 2, 1, 0] + [15, 11, 14, 10, 9, 8] + [31, 27, 30, 26, 25, 24]
    return trumpIdx, otherIdx

def getSuits(cards, suit, gameType):
    # TODO how can I use the fact that cards are sorted?!
    trumpIdx, _ = getCardOrder(gameType)
    suitCards =  [c for c in cards if c.suit == suit] # all suit cards with trumps
    return [c for c in suitCards if c.idx not in trumpIdx]

def getTrumps(cards, gameType):
    # TODO how can I use the fact that cards are sorted?!
    trumpIdx, _ = getCardOrder(gameType)
    trumps = []
    for c in cards:
        if c.idx in trumpIdx:
            trumps.append(c)
        else:
            return trumps 
    return trumps


def getCardByIdx(cards, idx):
    for i in cards:
        if i.idx == idx:
            return i
    return None  

def convertCards2Idx(cards):
    return [x.idx for x in cards]

# convert card or declaration to idx
def convert2Idx(inCardOrDecl):
    actionsIdx = []
    for i in inCardOrDecl:
        if isinstance(i, str):
            actionsIdx.append(32) # for weg
        else:
            actionsIdx.append(i.idx)
    return actionsIdx

def createCardByIdx(idx=0):
    return Card(SORTEDCARDS[idx][0], SORTEDCARDS[idx][1],idx)

def createDeclByIdx(idx=32):
    return "weg"

def createActionByIdx(idx=0):
    if idx>31:
        return createDeclByIdx(idx=idx)
    return createCardByIdx(idx=idx)

def convertIdx2CardMCTS(action_visits_dic):
    # action_visits_dic = {3: 4, 30: 3, 7: 3}
    return [createActionByIdx(x) for x  in action_visits_dic.keys()]


def sortCards(cards, gameType="RAMSCH"):
    trumpIdx, otherIdx = getCardOrder(gameType=gameType)
    cardOrder = trumpIdx + otherIdx
    idxSorted = sorted(convertCards2Idx(cards), key=cardOrder.index)
    cards     = [getCardByIdx(cards, x) for x in idxSorted]
    return cards

def getPoints(input_cards):
    #input_cards = [[card1, card2, card3, card4], [stich2], ...]
    # in class player
    result = 0
    for stich in input_cards:
        for card in stich:
            if card is not None:
                for cards_value, value in zip(["A", "X", "K", "O", "U"], [11, 10, 4, 3, 2]):
                    if card.rank == cards_value:
                        result += value
                        break
    return result

def getMoney(pointsArray, gameType="Ramsch"):
    res = [0]*4
    if gameType=="RAMSCH":
        #[0, <30, >30, >90] --> [15, 10, 5, 15x3]
        maxP = max(pointsArray)
        if maxP >= 90:
            res = [-15]*4
            res[pointsArray.index(maxP)] = 15*3
        else:
            for i,p in enumerate(pointsArray):
                if p != maxP:
                    if p==0 :   res[i] = 15
                    elif p<30 : res[i] = 10
                    else:       res[i] = 5    # p>=30
            looser = sum(res)*-1
            res[res.index(0)] = looser
    return res

def findCards(wantedCards, givenCards, max_equality=100):
    # wantedCards: [EO, GO] 
    # givenCards:  [E9, GO, GA, H9, E7, EK, GK, SO]
    # -> returns True
    wIdx = convertCards2Idx(wantedCards)
    gIdx = convertCards2Idx(givenCards)
    diff = list(set(wIdx).difference(set(gIdx)))
    if (1-len(diff)/len(wIdx))>=max_equality:
        return True
    return False

def createCardByName(name="EO"):
    suit = name[0]
    rank = name[1]
    idx=SORTEDCARDS.index(name)
    return Card(suit,rank,idx)

# remove printing formatting
def removeFormatting(res: str):
    res = res.replace("\033[1;33m","").replace("\033[1;32m","").replace("\033[1;31m","")
    return res.replace("\033[0;36m","").replace("\033[0m","").replace(" ","")

###
### Functions for MCTS
###
def getNextPlayer(cp):
    if cp == 3:
        return 0
    else:
        return cp+1

def subSample(playerCards, table, played, activeP, doEval=False):
    # playerCards consists of all hand cards -> doEval can be used
    # if playerCards consists only of hand card of activePlayer doEval cannot be used!
    hand         = playerCards[activeP]
    table        = [x for x in table if x is not None]
    allcards     = [x for x in range(32)]
    unknownCards = convertCards2Idx(hand+table+played)
    leftCards    = [i for i in allcards if i not in unknownCards]
    random.shuffle(leftCards)
    sampledCards   = [[], [], [], []]
    sampledCards[activeP] = convertCards2Idx(hand)
    tmp = activeP
    for _ in range(len(leftCards)):
        p = getNextPlayer(tmp)
        if p==activeP:
            p = getNextPlayer(p)
        sampledCards[p].append(leftCards.pop())
        tmp = p

    matching = [0, 0, 0, 0]
    if doEval: # do evaluation -> check similarity!
        for i in range(len(matching)):
            if not len(sampledCards[i])==len(playerCards[i]):
                print("ERROR!!!")
            intersec = len(set(sampledCards[i]).intersection(convertCards2Idx(playerCards[i])))
            matching[i] = round(intersec/len(playerCards[i]),2)
    return sampledCards, matching