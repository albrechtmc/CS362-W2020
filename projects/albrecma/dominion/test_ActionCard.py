from unittest import TestCase
import testUtility
import Dominion

class TestAction_card(TestCase):

    def setUp(self):
        #Data Setup
        self.players = testUtility.GetPlayernames()
        self.nV = testUtility.GetCurses(self.players)
        self.nC = testUtility.GetVictory(self.players)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GetSupply()

        #Pick n cards from box to be in the supply.
        self.supply = testUtility.LoadSupply(self.box, self.players, self.nV, self.nC)
        self.trash = []
        self.player = Dominion.Player('Annie')

        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 1



    def test_init(self):
        #initialize test data
        self.setUp()

        name = "Woodcutter"
        cost = 3
        actions = 0
        cards = 0
        buys = 1
        coins = 2

      #  actionCard = Dominion.Woodcutter(self.player.name, name, cost, actions, cards, buys, coins)
        actionCard = Dominion.Woodcutter()

        # verify that the class variables have the expected values
        self.assertEqual('Woodcutter', actionCard.name)
        self.assertEqual(cost, actionCard.cost)
        self.assertEqual(actions, actionCard.actions)
        self.assertEqual(cards, actionCard.cards)
        self.assertEqual(buys, actionCard.buys)
        self.assertEqual(coins, actionCard.coins)

    def test_use(self):
        #initialize test data
        self.setUp()

        actionCard = Dominion.Woodcutter()
        #Add the woodcutter card to the player's hand
        self.player.hand.append(actionCard)

        #Ensure the card is now in the hand and not in the trash
        self.assertIn(actionCard, self.player.hand)
        self.assertNotIn(actionCard, self.trash)

        #Use the action card (woodcutter)
        actionCard.use(self.player, self.trash)

        #Check if the action card is now in the played pile
        self.assertIn(actionCard, self.player.played)

        #check if the card is in the hand
        self.assertNotIn(actionCard, self.player.hand)

    def test_augment(self):
        # initialize test data
        self.setUp()

        actionCard = Dominion.Woodcutter()
        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 0
        initialHand = len(self.player.hand)

        actionCard.augment(self.player)

        #Woodcutter actions = 0, buys = 1, coins(purse) = 2
        #actions should be 0, buys 1, purse 2
        self.assertEqual(0, self.player.actions)
        self.assertEqual(1, self.player.buys)
        self.assertEqual(2, self.player.purse)

        #check the draw function
        finalHand = len(self.player.hand)
        #for woodcutter no cards should be drawn, so initial should match final
        self.assertEqual(initialHand, finalHand)

        #check against another card, the market
        actionCard = Dominion.Market()
        self.player.actions = 0
        self.player.buys = 0
        self.player.purse = 0
        initialHand = len(self.player.hand)

        actionCard.augment(self.player)

        #Market actions = 1, buys = 1, coins(purse) = 1
        #actions should be 1, buys 1, purse 1
        self.assertEqual(1, self.player.actions)
        self.assertEqual(1, self.player.buys)
        self.assertEqual(1, self.player.purse)

        #check the draw function
        finalHand = len(self.player.hand)
        # for market one card should be drawn, so initial + 1 should match final
        self.assertEqual(initialHand + 1, finalHand)