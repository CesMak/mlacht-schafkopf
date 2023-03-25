import unittest
from random import randrange
import gymnasium
import gym_schafkopf
from gym_schafkopf.envs.player import PlayerRANDOM 
from gym_schafkopf.envs.deck import Deck 

class TestPlayer(unittest.TestCase):

    def test_drawCards(self):
        # """
        # Test to draw cards
        # """
        pR = PlayerRANDOM("Markus")
        d  = Deck()
        d.shuffle()
        pR.draw(d, numCards=8)
        pR.sayHello()#"Hi! My name is Markus."
        assert len(pR.hand) == 8
    
    def test_showHand(self):
        d  = Deck(seed=1)
        d.shuffle()
        pR = PlayerRANDOM("Markus")
        pR.draw(d, numCards=8)
        print("\nunsorted List:", pR.hand)
        pR.getHandCardsSorted(gameType="RAMSCH")
        print("sorted List  :", pR.hand)
        assert pR.hand[0].getName() == "H9"
    
    def test_Options(self):
        pR = PlayerRANDOM("Markus")
        pRR= PlayerRANDOM("Hans")
        d  = Deck(seed=8)
        d.shuffle()
        pR.draw(d, numCards=8)
        pRR.draw(d, numCards=8)
        options_declaration = pR.getOptions(None, phase=0, gameType="RAMSCH")
        assert options_declaration[0]=="weg"
        opts       = pR.getOptions(None, phase=1, gameType="RAMSCH")
        assert len(opts) == 8 # empty table 8 cards can be played!

        # Test Playing options etc.:
        print("\n"+pR.name+" hand: "+str(pR.hand))
        for i in [1, 7, 6, 2,0]:
            print(pRR.name+" plays "+str(pRR.hand[i]))
            opts       = pR.getOptions(pRR.hand[i], phase=1, gameType="RAMSCH")
            print(pR.name+" can play now "+str(opts))
# for debugging and testing:
# if __name__ == "__main__":
#     unittest.main()