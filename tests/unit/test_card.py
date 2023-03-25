import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.card import Card 

class TestCard(unittest.TestCase):

    def test_create_cards(self):
        # """
        # Test to create a random card
        # """
        cards = []
        i     = 0 
        for s in ["E", "G", "H", "S"]:
            for r in ["7", "8", "9", "1", "U", "O", "K", "A"]:
                cards.append(Card(s, r, i))
                i+=1
        assert cards[0].show()        == "\033[1;33m"+"E7"+"\033[0m"
        assert cards[0].show_simple() == "E7_0"