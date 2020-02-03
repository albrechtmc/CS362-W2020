from unittest import TestCase
import testUtility
import Dominion

class Test(TestCase):

    def setUp(self):
        #Data Setup
        self.players = testUtility.GetPlayernames()
        self.nV = testUtility.GetCurses(self.players)
        self.nC = testUtility.GetVictory(self.players)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GetSupply()

        #Pick n cards from box to be in the supply.
        self.supply = testUtility.GetSupplyBox(self.box)
        testUtility.LoadSupply(self.supply, self.players, self.nV, self.nC)
        self.trash = []
        self.player = Dominion.Player('Annie')


    def test_gameover(self):

        #run the setup
        self.setUp()
        #check the state of the game after setup.
        returnGameState = Dominion.gameover(self.supply)
        #ensure the game is not over after setup
        self.assertEqual(False, returnGameState)
        #remove all of the provinces to force a game over
        self.supply["Province"] = [Dominion.Province()] * 0
        #rerun gameover()
        returnGameState = Dominion.gameover(self.supply)
        #ensure the game is over
        self.assertEqual(True, returnGameState)
        #add some provinces back
        self.supply["Province"] = [Dominion.Province()] * 3
        #rerun gameover()
        returnGameState = Dominion.gameover(self.supply)
        #ensure the game is not over
        self.assertEqual(False, returnGameState)
        #empty 2 stacks, in this case copper and silver
        self.supply["Copper"] = [Dominion.Copper()] * 0
        self.supply["Silver"] = [Dominion.Silver()] * 0
        #rerun gameover()
        returnGameState = Dominion.gameover(self.supply)
        #ensure the game is not over
        self.assertEqual(False, returnGameState)

        #empty tbe third stack, gold, to force a gameover
        self.supply["Gold"] = [Dominion.Gold()] * 0
        #rerun gameover()
        returnGameState = Dominion.gameover(self.supply)
        #ensure the game is not over
        self.assertEqual(True, returnGameState)
