import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.schafkopf import Schafkopf 
from gym_schafkopf.envs.helper    import findCards, createCardByName, subSamplev2, subSample, createActionByIdx, convertIdx2CardMCTS,deleteFolder, createCardsByIdx, sortCards, evaluateTable, createTable
from gym_schafkopf.envs.mcts.mct  import MonteCarloTree
from copy import deepcopy
from datetime import datetime

# Seeds list:
# 56681 -> [EO, S8, HU, HO, SU, SO, GU, EU] player0
# 1170  -> [EO, GO, EU, GU, HU, EA, E9, SA] player0

def findSeed(givenCards, equality=0.9):
    for i in range(100000):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": i, "active_player": 0, "print_": 0}
        s = Schafkopf(options_dict=options)
        print("Testing a Schafkopf Game:")
        s.setup_game()
        hand_Cards = s.players[0].hand
        gCards = [createCardByName(g) for g in givenCards]
        if(findCards(gCards, hand_Cards, equality)):
            print(hand_Cards)
            return i
    return None

def runFullGame(options):
    s = Schafkopf(options)
    s.setup_game()
    for _ in range(36):
        s.step()
    return s.players

class TestSchafkopf(unittest.TestCase):
    def test_RAMSCH_NORMAL(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 21, "active_player": 0, "print_": 1}
        s = Schafkopf(options_dict=options)
        print("Testing a Schafkopf Game:")
        s.setup_game()
        for _ in range(36):
            s.step()
        players = s.players
        money   = [p.money for p in players]
        points  = [p.points for p in players]
        assert s.movesIdx          == [32, 32, 32, 32, 30, 27, 24, 31, 19, 22, 29, 28, 5, 1, 18, 20, 17, 2, 4, 13, 6, 0, 3, 8, 11, 12, 9, 7, 21, 10, 16, 14, 23, 15, 25, 26]
        assert s.initialHandsIdx   == [[13, 20, 22, 6, 15, 10, 9, 30], [5, 29, 17, 16, 7, 0, 27, 25], [28, 3, 2, 1, 11, 14, 26, 24], [21, 4, 12, 23, 19, 18, 8, 31]]
        assert [5, 24, 14, 77]  == points
        assert [10, 10, 10, -30] == money

    def test_DURCHMARSCH(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 1170, "active_player": 0, "print_": 1}
        s = Schafkopf(options_dict=options)
        s.setup_game()
        for _ in range(36):
            s.step()
        players = s.players
        money   = [p.money for p in players]
        points  = [p.points for p in players]
        assert s.movesIdx          == [32, 32, 32, 32, 2, 6, 3, 0, 16, 29, 20, 18, 9, 12, 14, 8, 7, 25, 10, 1, 13, 21, 28, 19, 31, 27, 24, 26, 4, 15, 23, 22, 5, 11, 17, 30]
        assert s.initialHandsIdx   == [[5, 13, 4, 12, 20, 7, 2, 31], [21, 18, 6, 15, 11, 14, 27, 25], [28, 23, 17, 16, 3, 10, 8, 24], [29, 19, 22, 1, 0, 9, 30, 26]]
        assert [101, 0, 14, 5]      == points
        assert [45, -15, -15, -15] == money

    def test_subSample(self):
        # TODO convert this test to use subSamplev2 as subSample is deprecated!
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 1170, "active_player": 0, "print_": 1}
        s = Schafkopf(options_dict=options)
        s.setup_game()
        for _ in range(26):
            s.step()
        players     = s.players
        aP          =  s.active_player
        playerCards = [x.hand for x in players]
        playedCards = []
        for i in [x.offhand for x in players]:
            playedCards.extend(i)
        playedCards_flat = sum(playedCards, [])
        enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=True)
        assert s.movesIdx        == [32, 32, 32, 32, 2, 6, 3, 0, 16, 29, 20, 18, 9, 12, 14, 8, 7, 25, 10, 1, 13, 21, 28, 19, 31, 27]
        assert s.initialHandsIdx == [[5, 13, 4, 12, 20, 7, 2, 31], [21, 18, 6, 15, 11, 14, 27, 25], [28, 23, 17, 16, 3, 10, 8, 24], [29, 19, 22, 1, 0, 9, 30, 26]]
        assert matching == [0.5, 0.0, 1.0, 0.33]

        print("\nDo 2 more steps and subsample again with doEval=False and only a valid state as input")
        for _ in range(2):
            s.step()
        aP          = s.active_player
        playerCards = [[],[],[],[]]
        playerCards[aP] = players[aP].hand
        playedCards = []
        for i in [x.offhand for x in players]:
            playedCards.extend(i)
        playedCards_flat = sum(playedCards, [])
        enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=False)
        assert matching == [0, 0, 0, 0]
        print(enemySubSamples, matching)

        print("\nDo 1 more step and create multiple subsamples -> there are still so many possibilitys")
        s.step()
        playerCards = [x.hand for x in players]
        playedCards = []
        for i in [x.offhand for x in players]:
            playedCards.extend(i)
        playedCards_flat = sum(playedCards, [])
        for i in range(5):
            enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=True)
            #assert matching == [0.5, 0.5, 1.0, 0.33]
            print(enemySubSamples, matching)

    def test_replayGame(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": None, "active_player": 0, "print_": 1}
        s = Schafkopf(options)
        s.setup_game()
        for _ in range(26):
            s.step()

        s2 = Schafkopf(options)
        s2.replayGame(moves=s.movesIdx, handCards=s.initialHandsIdx)
        assert s.initialHandsIdx == s2.initialHandsIdx
        assert s.movesIdx        == s2.movesIdx

    def test_mcts(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 121, "active_player": 0, "print_": 1}
        s = Schafkopf(options)
        s.setup_game()
        for _ in range(5):
            s.step()
        gS = s.getGameState()
        gS["options"]["print_"] = 0   # print during replays when mcts searches best move?

        mct =  MonteCarloTree(gS, s, ucb_const=1)
        mcts_action = mct.uct_search(20, print_=False)
        best_action = max(mcts_action, key=mcts_action.get)
        print("mcts actions and visits:", mcts_action, convertIdx2CardMCTS(mcts_action), "best action->", best_action, createActionByIdx(best_action))

    def test_mcts_RAMSCH_DURCHMARSCH(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_20", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 1}
        s = Schafkopf(options)
        s.setup_game()
        for _ in range(36):
            s.step()

    def test_mcts_options(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
        s = Schafkopf(options)
        s.setup_game()
        # default case:
        assert s.players[1].num_playouts  == 50
        assert s.players[1].num_subSamples == 10

        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_1_2", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
        s = Schafkopf(options)
        s.setup_game()
        assert s.players[1].num_playouts  == 2
        assert s.players[1].num_subSamples ==1

        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_4", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
        s = Schafkopf(options)
        s.setup_game()
        assert s.players[1].num_playouts  == 50
        assert s.players[1].num_subSamples ==4


        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
        s = Schafkopf(options)
        s.setup_game()
        assert s.players[1].num_playouts  == 50
        assert s.players[1].num_subSamples ==-1

        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_10", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
        s = Schafkopf(options)
        s.setup_game()
        assert s.players[1].num_playouts  == 10
        assert s.players[1].num_subSamples ==-1

    def test_mcts_RAMSCH_NORMAL(self):
        options          = ["RANDOM", "MCTS_OFF_10", "MCTS_OFF_50", "MCTS_OFF_90",  "MCTS_2_10", "MCTS_5_10", "MCTS_10_50"]
        expectedMoneyLea = [-30,        -25          ,  5         ,             10,            -25,        5       , 5]
        for (j,m)  in zip(options, expectedMoneyLea):
            oM = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", j, "RANDOM", "RANDOM"], "seed": 125, "active_player": 0, "print_": 0}
            players = runFullGame(oM)
            assert players[1].money == m, "Lea: "+j+" Expected "+str(m)+" for Lea but got:"+str(players[1].money)

    #@unittest.skip("This Test runs longer than 4min -> is no unit Test skip it!")
    def test_mcts_benchmark(self):
        res = [0, 0, 0, 0]
        total_time = datetime.now()
        diff        = datetime.now()

        # Random Game:
        for i in range(15):
            oM = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": i, "active_player": 0, "print_": 0}
            p = runFullGame(oM)
            for j,pp in enumerate(p):
                res[j] +=pp.money
        print(oM["type"], res, (datetime.now()-diff))
        diff = datetime.now()
        res = [0, 0, 0, 0]
        # MCTS Game
        for subsample in ["OFF", "10", "20", "30"]:
            for playouts in ["10", "20", "50", "80"]:
                for ucb in ["10", "50", "100", "200", "300", "400", "1000"]:
                    for i in range(15):
                        oM = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "MCTS_"+subsample+"_"+playouts+"_"+ucb, "RANDOM"], "seed": i, "active_player": 0, "print_": 0}
                        p = runFullGame(oM)
                        for j,pp in enumerate(p):
                            res[j] +=pp.money
                    print(oM["type"], res, (datetime.now()-diff))
                    diff = datetime.now()
                    res = [0, 0, 0, 0]
        # optimal ucb const: 200?!  
        print("Total time:", datetime.now()-total_time)
        # see benchmark at end of file!

    def test_mcts_tree(self):
        # save a MCTS Tree
        deleteFolder("tests/unit/trees/")
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_80_50", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 1, "save_tree": 1}
        s = Schafkopf(options)
        s.setup_game()
        for _ in range(12):
            s.step()

    def test_subSampleV2(self):
        # play some steps then subsample!
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 1170, "active_player": 0, "print_": 1}
        s = Schafkopf(options_dict=options)
        s.setup_game()
        for _ in range(26):
            s.step()
        players     = s.players
        aP          =  s.active_player
        ownHand     = players[aP].hand
        playerCards = subSamplev2(s.movesIdx, aP, ownHand)
        for sampled,trueC in zip(playerCards, s.initialHandsIdx):
            intersec = len(set(sampled).intersection(trueC))
            perc     = round(intersec/8*100,1)
            print(createCardsByIdx(trueC), "-->", sortCards(createCardsByIdx(sampled)), intersec, "-->", str(perc)+"%")
        assert playerCards       == [[2, 20, 12, 7, 13, 31, 5, 26], [6, 18, 14, 25, 21, 27, 22, 4], [3, 16, 8, 10, 28, 23, 17, 24], [0, 29, 9, 1, 19, 30, 15, 11]]

    def test_EvaluateTable(self):
        table = createTable(["S8", "SX", "S9", "EX"])
        hightestCard, playerWithHighestCard, points = evaluateTable(table, "RAMSCH", table[0])
        assert hightestCard.idx == 27 # SX
        assert playerWithHighestCard == 1
        assert points == 20
        hightestCard, playerWithHighestCard, points = evaluateTable(table, "RAMSCH", table[3])
        assert hightestCard.idx == 3 # EX
        assert playerWithHighestCard == 3
        assert points == 20

    @unittest.skip("This Test requires user(keyboard) inputs -> skip it!")
    def test_HUMANKEYBOARD(self):
        # play some steps then subsample!
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["HUMAN", "MCTS_20_50_200", "MCTS_20_50_200", "MCTS_20_50_200"], "seed": 451, "active_player": 0, "print_": 1, "save_tree": 0}
        s = Schafkopf(options_dict=options)
        s.setup_game()
        for _ in range(36):
            s.step()

        # TODO ML: irgendwas kann noch nicht stimmen 
        # MCTS Player ist nur minimal besser als der RANDOM spieler?! mit erheblichem Aufwand???!!!
        # GUT Ist jedoch schonmal dass er im offFall recht gut ist. 
        # vllt. funktioniert das subsamplev2 noch immer nicht richtig!!! 
        # auto option and time measurement for mcts step?

##for debugging and testing:
if __name__ == "__main__":
    unittest.main()

# Find seeds with:
# cards = ["EO", "GO", "SO", "HO", "EU", "GU", "HU", "SU"]
# print(findSeed(cards, equality=0.7))




# Benchmark MCTS one Player
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_10', 'RANDOM'] [-160, 110, 110, -60] 0:00:02.007400
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_50', 'RANDOM'] [-142.5, 125, 85, -67.5] 0:00:01.993447
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_100', 'RANDOM'] [-155, 125, 95, -65] 0:00:01.943524
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_200', 'RANDOM'] [-160, 130, 95, -65] 0:00:01.957479
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_300', 'RANDOM'] [-95, 105, 50, -60] 0:00:02.192812
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_400', 'RANDOM'] [-95, 105, 50, -60] 0:00:02.644976
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_10_1000', 'RANDOM'] [-95, 105, 50, -60] 0:00:03.017063
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_10', 'RANDOM'] [-110, 115, 70, -75] 0:00:05.703681
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_50', 'RANDOM'] [-175, 175, 85, -85] 0:00:05.491224
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_100', 'RANDOM'] [-185, 105, 120, -40] 0:00:05.677411
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_200', 'RANDOM'] [-155, 25, 165, -35] 0:00:05.652956
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_300', 'RANDOM'] [-160, -5, 170, -5] 0:00:05.583390
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_400', 'RANDOM'] [-160, -5, 170, -5] 0:00:04.747048
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_20_1000', 'RANDOM'] [-125, 30, 135, -40] 0:00:03.482563
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_10', 'RANDOM'] [-170, 155, 115, -100] 0:00:08.732799
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_50', 'RANDOM'] [-65, 130, 65, -130] 0:00:09.052980
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_100', 'RANDOM'] [-130, 85, 105, -60] 0:00:09.322410
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_200', 'RANDOM'] [-160, 100, 170, -110] 0:00:13.237513
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_300', 'RANDOM'] [-170, 105, 140, -75] 0:00:10.761275
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_400', 'RANDOM'] [-170, 105, 140, -75] 0:00:09.360959
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_50_1000', 'RANDOM'] [-85.0, 90, 85, -90.0] 0:00:08.535611
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_10', 'RANDOM'] [-55, 90, 85, -120] 0:00:17.840673
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_50', 'RANDOM'] [-180, 125, 75, -20] 0:00:16.388665
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_100', 'RANDOM'] [-120, 75, 65, -20] 0:00:14.290495
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_200', 'RANDOM'] [-155, 95, 120, -60] 0:00:14.573909
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_300', 'RANDOM'] [-120, 120, 120, -120] 0:00:16.992466
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_400', 'RANDOM'] [-75, 95, 80, -100] 0:00:17.834897
        # ['RANDOM', 'RANDOM', 'MCTS_OFF_80_1000', 'RANDOM'] [-130, 95, 75, -40] 0:00:13.988913
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_10', 'RANDOM'] [-110, 120, 65, -75] 0:00:21.219812
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_50', 'RANDOM'] [-110, 120, 65, -75] 0:00:24.250880
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_100', 'RANDOM'] [-110, 120, 65, -75] 0:00:20.889986
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_200', 'RANDOM'] [-110, 120, 65, -75] 0:00:23.109078
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_300', 'RANDOM'] [-110, 120, 65, -75] 0:00:21.387712
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_400', 'RANDOM'] [-110, 120, 65, -75] 0:00:23.085678
        # ['RANDOM', 'RANDOM', 'MCTS_10_10_1000', 'RANDOM'] [-110, 120, 65, -75] 0:00:21.825071
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_10', 'RANDOM'] [-50, 80, 85, -115] 0:00:40.824571
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_50', 'RANDOM'] [-50, 80, 85, -115] 0:00:40.536765
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_100', 'RANDOM'] [-50, 80, 85, -115] 0:00:42.048412
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_200', 'RANDOM'] [-50, 80, 85, -115] 0:00:40.513044
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_300', 'RANDOM'] [-50, 80, 85, -115] 0:00:39.851259
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_400', 'RANDOM'] [-50, 80, 85, -115] 0:00:39.877120
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_1000', 'RANDOM'] [-50, 80, 85, -115] 0:00:41.135376
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_10', 'RANDOM'] [120, 25, -10, -135] 0:01:30.681763
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_50', 'RANDOM'] [120, 25, -10, -135] 0:01:31.646014
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_100', 'RANDOM'] [120, 25, -10, -135] 0:01:32.253166
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_200', 'RANDOM'] [120, 25, -10, -135] 0:01:29.756848
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_300', 'RANDOM'] [120, 25, -10, -135] 0:01:30.148696
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_400', 'RANDOM'] [120, 25, -10, -135] 0:01:30.282228
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_1000', 'RANDOM'] [120, 25, -10, -135] 0:01:29.943735
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_10', 'RANDOM'] [-105, 60, 110, -65] 0:02:27.044272
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_50', 'RANDOM'] [-105, 60, 110, -65] 0:02:21.881870
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_100', 'RANDOM'] [-105, 60, 110, -65] 0:02:23.001645
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_200', 'RANDOM'] [-105, 60, 110, -65] 0:02:25.238219
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_300', 'RANDOM'] [-105, 60, 110, -65] 0:02:27.116918
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_400', 'RANDOM'] [-105, 60, 110, -65] 0:02:29.413822
        # ['RANDOM', 'RANDOM', 'MCTS_10_80_1000', 'RANDOM'] [-105, 60, 110, -65] 0:02:28.011865
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_10', 'RANDOM'] [5, 85, -30, -60] 0:00:43.140565
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_50', 'RANDOM'] [5, 85, -30, -60] 0:00:43.699808
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_100', 'RANDOM'] [5, 85, -30, -60] 0:00:43.217509
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_200', 'RANDOM'] [5, 85, -30, -60] 0:00:43.327822
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_300', 'RANDOM'] [5, 85, -30, -60] 0:00:43.367453
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_400', 'RANDOM'] [5, 85, -30, -60] 0:00:42.885367
        # ['RANDOM', 'RANDOM', 'MCTS_20_10_1000', 'RANDOM'] [5, 85, -30, -60] 0:00:42.894916
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_10', 'RANDOM'] [-80, 100, 80, -100] 0:01:18.218780
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_50', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.949795
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_100', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.807103
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_200', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.672612
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_300', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.551208
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_400', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.989084
        # ['RANDOM', 'RANDOM', 'MCTS_20_20_1000', 'RANDOM'] [-80, 100, 80, -100] 0:01:17.798866
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_10', 'RANDOM'] [10, 40, 50, -100] 0:02:57.620850
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_50', 'RANDOM'] [10, 40, 50, -100] 0:02:56.322627
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_100', 'RANDOM'] [10, 40, 50, -100] 0:02:56.778613
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_200', 'RANDOM'] [10, 40, 50, -100] 0:02:56.694615
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_300', 'RANDOM'] [10, 40, 50, -100] 0:02:56.118454
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_400', 'RANDOM'] [10, 40, 50, -100] 0:02:56.949109
        # ['RANDOM', 'RANDOM', 'MCTS_20_50_1000', 'RANDOM'] [10, 40, 50, -100] 0:02:57.169749
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_10', 'RANDOM'] [-155, 65, 110, -20] 0:04:56.824123
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_50', 'RANDOM'] [-155, 65, 110, -20] 0:04:58.563570
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_100', 'RANDOM'] [-155, 65, 110, -20] 0:05:00.219707
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_200', 'RANDOM'] [-155, 65, 110, -20] 0:04:59.501111
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_300', 'RANDOM'] [-155, 65, 110, -20] 0:04:55.936276
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_400', 'RANDOM'] [-155, 65, 110, -20] 0:05:02.332643
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_1000', 'RANDOM'] [-155, 65, 110, -20] 0:04:59.522420
        # Total time: 1:48:28.061632