import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.schafkopf import Schafkopf 
from gym_schafkopf.envs.helper    import findCards, createCardByName, subSamplev2, subSample, createActionByIdx, convertIdx2CardMCTS,deleteFolder, createCardsByIdx, sortCards, evaluateTable, createTable
from gym_schafkopf.envs.mcts.mct  import MonteCarloTree

class TestSchafkopf(unittest.TestCase):
    #@unittest.skip("This Test requires user(keyboard) inputs -> skip it!")
    def test_HUMANKEYBOARD(self):
        options = {"names": ["Max", "Lea", "Jo", "Tim"], "type": ["HUMAN", "MCTS_20_50_200", "MCTS_20_50_200", "MCTS_20_50_200"], "seed": 451, "active_player": 0, "print_": 1, "save_tree": 0}
        s = Schafkopf(options_dict=options)
        s.setup_game()
        for _ in range(36):
            s.step()

##for debugging and testing:
if __name__ == "__main__":
    unittest.main()