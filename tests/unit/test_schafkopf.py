import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.schafkopf import Schafkopf 
from gym_schafkopf.envs.helper    import findCards, createCardByName, subSample, createActionByIdx, convertIdx2CardMCTS,deleteFolder
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
    # def test_RAMSCH_NORMAL(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 21, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options_dict=options)
    #     print("Testing a Schafkopf Game:")
    #     s.setup_game()
    #     for _ in range(36):
    #         s.step()
    #     players = s.players
    #     money   = [p.money for p in players]
    #     points  = [p.points for p in players]
    #     assert s.movesIdx          == [32, 32, 32, 32, 30, 27, 24, 31, 19, 22, 29, 28, 5, 1, 18, 20, 17, 2, 4, 13, 6, 0, 3, 8, 11, 12, 9, 7, 21, 10, 16, 14, 23, 15, 25, 26]
    #     assert s.initialHandsIdx   == [[13, 20, 22, 6, 15, 10, 9, 30], [5, 29, 17, 16, 7, 0, 27, 25], [28, 3, 2, 1, 11, 14, 26, 24], [21, 4, 12, 23, 19, 18, 8, 31]]
    #     assert [5, 24, 14, 77]  == points
    #     assert [10, 10, 10, -30] == money

    # def test_DURCHMARSCH(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 1170, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options_dict=options)
    #     s.setup_game()
    #     for _ in range(36):
    #         s.step()
    #     players = s.players
    #     money   = [p.money for p in players]
    #     points  = [p.points for p in players]
    #     assert s.movesIdx          == [32, 32, 32, 32, 2, 6, 3, 0, 16, 29, 20, 18, 9, 12, 14, 8, 7, 25, 10, 1, 13, 21, 28, 19, 31, 27, 24, 26, 4, 15, 23, 22, 5, 11, 17, 30]
    #     assert s.initialHandsIdx   == [[5, 13, 4, 12, 20, 7, 2, 31], [21, 18, 6, 15, 11, 14, 27, 25], [28, 23, 17, 16, 3, 10, 8, 24], [29, 19, 22, 1, 0, 9, 30, 26]]
    #     assert [101, 0, 14, 5]      == points
    #     assert [45, -15, -15, -15] == money

    # def test_subSample(self):
    #     # TODO convert this test to use subSamplev2 as subSample is deprecated!
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 1170, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options_dict=options)
    #     s.setup_game()
    #     for _ in range(26):
    #         s.step()
    #     players     = s.players
    #     aP          =  s.active_player
    #     playerCards = [x.hand for x in players]
    #     playedCards = []
    #     for i in [x.offhand for x in players]:
    #         playedCards.extend(i)
    #     playedCards_flat = sum(playedCards, [])
    #     enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=True)
    #     assert s.movesIdx        == [32, 32, 32, 32, 2, 6, 3, 0, 16, 29, 20, 18, 9, 12, 14, 8, 7, 25, 10, 1, 13, 21, 28, 19, 31, 27]
    #     assert s.initialHandsIdx == [[5, 13, 4, 12, 20, 7, 2, 31], [21, 18, 6, 15, 11, 14, 27, 25], [28, 23, 17, 16, 3, 10, 8, 24], [29, 19, 22, 1, 0, 9, 30, 26]]
    #     assert matching == [0.5, 0.0, 1.0, 0.33]

    #     print("\nDo 2 more steps and subsample again with doEval=False and only a valid state as input")
    #     for _ in range(2):
    #         s.step()
    #     aP          = s.active_player
    #     playerCards = [[],[],[],[]]
    #     playerCards[aP] = players[aP].hand
    #     playedCards = []
    #     for i in [x.offhand for x in players]:
    #         playedCards.extend(i)
    #     playedCards_flat = sum(playedCards, [])
    #     enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=False)
    #     assert matching == [0, 0, 0, 0]
    #     print(enemySubSamples, matching)

    #     print("\nDo 1 more step and create multiple subsamples -> there are still so many possibilitys")
    #     s.step()
    #     playerCards = [x.hand for x in players]
    #     playedCards = []
    #     for i in [x.offhand for x in players]:
    #         playedCards.extend(i)
    #     playedCards_flat = sum(playedCards, [])
    #     for i in range(5):
    #         enemySubSamples, matching = subSample(playerCards, s.table, playedCards_flat, aP, doEval=True)
    #         #assert matching == [0.5, 0.5, 1.0, 0.33]
    #         print(enemySubSamples, matching)

    # def test_replayGame(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": None, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     for _ in range(26):
    #         s.step()

    #     s2 = Schafkopf(options)
    #     s2.replayGame(moves=s.movesIdx, handCards=s.initialHandsIdx)
    #     assert s.initialHandsIdx == s2.initialHandsIdx
    #     assert s.movesIdx        == s2.movesIdx

    # def test_mcts(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", "RANDOM", "RANDOM"], "seed": 121, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     for _ in range(5):
    #         s.step()
    #     gS = s.getGameState()
    #     gS["options"]["print_"] = 0   # print during replays when mcts searches best move?

    #     mct =  MonteCarloTree(gS, s, ucb_const=1)
    #     mcts_action = mct.uct_search(20, print_=False)
    #     best_action = max(mcts_action, key=mcts_action.get)
    #     print("mcts actions and visits:", mcts_action, convertIdx2CardMCTS(mcts_action), "best action->", best_action, createActionByIdx(best_action))

    # def test_mcts_RAMSCH_DURCHMARSCH(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_20", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 1}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     for _ in range(36):
    #         s.step()

    # def test_mcts_options(self):
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     # default case:
    #     assert s.players[1].num_playouts  == 50
    #     assert s.players[1].num_subSamples == 10

    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_1_2", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     assert s.players[1].num_playouts  == 2
    #     assert s.players[1].num_subSamples ==1

    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_4", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     assert s.players[1].num_playouts  == 50
    #     assert s.players[1].num_subSamples ==4


    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     assert s.players[1].num_playouts  == 50
    #     assert s.players[1].num_subSamples ==-1

    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_10", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 0}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     assert s.players[1].num_playouts  == 10
    #     assert s.players[1].num_subSamples ==-1

    # def test_mcts_RAMSCH_NORMAL(self):
    #     options          = ["RANDOM", "MCTS_OFF_10", "MCTS_OFF_50", "MCTS_OFF_90",  "MCTS_2_10", "MCTS_5_10", "MCTS_10_50"]
    #     expectedMoneyLea = [-30,        5          ,  -25         ,             5,            -30,        -30       , 10]
    #     for (j,m)  in zip(options, expectedMoneyLea):
    #         oM = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", j, "RANDOM", "RANDOM"], "seed": 125, "active_player": 0, "print_": 0}
    #         players = runFullGame(oM)
    #         assert players[1].money == m, "Lea: "+j+" Expected "+str(m)+" for Lea but got:"+str(players[1].money)

    #     # TODO check if subsample v2 really works correctly!!!!
    #     # CHECK WHY oMCTS_10_50 is better than oMCTS_OFF_90??
    #     # oMCTS_OFF_90: SO, SX, E7, EU, GX, E9, EO, HO <- this is how Lea plays cards
    #     # oMCTS_OFF_50: SO, SX, EU,                    <- this is how lea plays cards
    #     # reason: cause other players play other cards that might be better for LEA

    # @unittest.skip("This Test runs longer than 4min -> is no unit Test skip it!")
    def test_mcts_benchmark(self):
        res = [0, 0, 0, 0]
        total_time = datetime.now()
        diff        = datetime.now()
        print("Benchmark MCTS one Player")
        for j in ["RANDOM", "MCTS_10_20_50", "MCTS_10_50_50", "MCTS_20_80_50"]:
            for i in range(15):
                oM = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "RANDOM", j, "RANDOM"], "seed": i, "active_player": 0, "print_": 1}
                p = runFullGame(oM)
                for i,pp in enumerate(p):
                    res[i] +=pp.money
            print(oM["type"], res, (datetime.now()-diff))
            diff = datetime.now()
        print("Total time:", datetime.now()-total_time)
        # Result: 
        # ['RANDOM', 'RANDOM', 'RANDOM', 'RANDOM']        [-130.0, 110, 115.0, -95] 0:00:00.008686
        # ['RANDOM', 'RANDOM', 'MCTS_10_20_50', 'RANDOM'] [-252.5, 177.5, 185.0, -110.0] 0:00:26.108119
        # ['RANDOM', 'RANDOM', 'MCTS_10_50_50', 'RANDOM'] [-322.5, 282.5, 195.0, -155.0] 0:01:08.743489
        # ['RANDOM', 'RANDOM', 'MCTS_20_80_50', 'RANDOM'] [-437.5, 392.5, 205.0, -160.0] 0:03:59.666439

    # def test_mcts_tree(self):
    #     deleteFolder("tests/unit/trees/")
    #     options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["RANDOM", "MCTS_OFF_80_50", "RANDOM", "RANDOM"], "seed": 56681, "active_player": 0, "print_": 1, "save_tree": 1}
    #     s = Schafkopf(options)
    #     s.setup_game()
    #     for _ in range(12):
    #         s.step()

        # when printing tree works make some more evaluation regarding ucb const as well!
        # auto option and time measurement for mcts step?

##for debugging and testing:
if __name__ == "__main__":
    unittest.main()

# Find seeds with:
# cards = ["EO", "GO", "SO", "HO", "EU", "GU", "HU", "SU"]
# print(findSeed(cards, equality=0.7))
