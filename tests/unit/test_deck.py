import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.deck import Deck 
from gym_schafkopf.envs.helper    import removeFormatting

class TestDeck(unittest.TestCase):

    def test_create_deck(self):
        # """
        # Test to create a deck
        # """
        d = Deck()
        res = d.show()
        res = removeFormatting(res)
        assert res == "E7,E8,E9,EX,EU,EO,EK,EA,G7,G8,G9,GX,GU,GO,GK,GA,H7,H8,H9,HX,HU,HO,HK,HA,S7,S8,S9,SX,SU,SO,SK,SA,"
    
    def test_shuffle_deck(self):
        d = Deck()
        d.shuffle()
        res = d.show()
        res = removeFormatting(res)
        assert res != "E7,E8,E9,EX,EU,EO,EK,EA,G7,G8,G9,GX,GU,GO,GK,GA,H7,H8,H9,HX,HU,HO,HK,HA,S7,S8,S9,SX,SU,SO,SK,SA,"

        d.deal()
        assert len(d.cards) == 31