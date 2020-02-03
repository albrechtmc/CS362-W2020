from unittest import TestCase
import testUtility
import Dominion

class TestPlayer(TestCase):

    def setUp(self):
        #Data Setup
        self.players = testUtility.GetPlayernames()
        #self.deck = [Dominion.Woodcutter()]
        #self.hand = [Dominion.Woodcutter()]
        self.nV = testUtility.GetCurses(self.players)
        self.nC = testUtility.GetVictory(self.players)
        self.box = testUtility.GetBoxes(self.nV)
        self.supply_order = testUtility.GetSupply()

        #Pick n cards from box to be in the supply.
        self.supply = testUtility.LoadSupply(self.box, self.players, self.nV, self.nC)
        self.trash = []
        self.player = Dominion.Player('Annie')


    def test_draw(self):

        #ensure we start with 5 cards in the hand
        self.assertEqual(len(self.player.hand), 5)
        self.player.draw(None)
        #after drawing a card, there should be 6 cards in the hand
        self.assertEqual(len(self.player.hand), 6)

        #empty the players deck to test deck replentishment
        self.player.deck = []
        discardSize = len(self.player.discard)
        self.assertEqual(len(self.player.deck), 0)

        self.player.draw(None)
        #compare the length of the saved discardSize to the length of the deck
        self.assertEqual(discardSize, len(self.player.deck))
        #ensure the discard is empty
        self.assertEqual(0, len(self.player.discard))

        #stack the deck with cards
        self.player.deck = [Dominion.Copper()]*7 + [Dominion.Estate()]*3

        #ensure there are cards in the deck
        self.assertGreater(len(self.player.deck), 0)
        deckSize = len(self.player.deck)
        self.player.draw()

        #ensure the card was removed from the deck
        self.assertGreater(deckSize, len(self.player.deck))


    def test_action_balance(self):
        #add a woodcutter card to ensure there is an action card in the deck
        self.player.deck.append(Dominion.Woodcutter())
        balance = 0
        for c in self.player.stack():
            if c.category == "action":
                balance = balance - 1 + c.actions
        returnVal = 70* balance / len(self.player.stack())

        funcVal = self.player.action_balance()

        #ensure balance is -1 following addition of woodcutter
        self.assertEqual(-1, balance)
        #ensure the return value of the function is equal to the return value expected with one woodcutter
        self.assertEqual(returnVal, funcVal)

    def test_cardsummary(self):
        #test the base deck
        summary = {}
        for c in self.player.stack():
            if c.name in summary:
                summary[c.name] += 1
            else:
                summary[c.name] = 1
        summary['VICTORY POINTS'] = self.player.calcpoints()

        funcVal = self.player.cardsummary()

        #ensure the complete summary matches what is expected
        self.assertEqual(funcVal, summary)
        #ensure there are 3 victory points
        self.assertEqual(funcVal['VICTORY POINTS'], 3)
        # ensure there are 7 copper
        self.assertEqual(funcVal['Copper'], 7)
        # ensure there are 3 estates
        self.assertEqual(funcVal['Estate'], 3)

        #add a woodcutter card and ensure it was correctly tallied
        self.player.deck.append(Dominion.Woodcutter())
        summary = {}
        for c in self.player.stack():
            if c.name in summary:
                summary[c.name] += 1
            else:
                summary[c.name] = 1
        summary['VICTORY POINTS'] = self.player.calcpoints()

        funcVal = self.player.cardsummary()

        # ensure the complete summary matches what is expected
        self.assertEqual(funcVal, summary)
        # ensure there is a woodcutter
        self.assertEqual(funcVal['Woodcutter'], 1)
        #ensure there are 3 victory points
        self.assertEqual(funcVal['VICTORY POINTS'], 3)
        # ensure there are 7 copper
        self.assertEqual(funcVal['Copper'], 7)
        # ensure there are 3 estates
        self.assertEqual(funcVal['Estate'], 3)


    def test_calcpoints(self):

        tally = 0
        gardens = 0
        n = 0
        for c in self.player.stack():
            tally += c.vpoints
            n += 1
            if c.name == "Gardens":
                gardens+=1
        returnVal = tally + n//10 * gardens

        funcVal = self.player.calcpoints()

        #ensure the testfunction matches what is expected
        self.assertEqual(funcVal, returnVal)
        #ensure the total victory points is 3 (for 3 estates)
        self.assertEqual(funcVal, 3)

        #add a province card to add 6 vp to the total expected
        self.player.deck.append(Dominion.Province())
        funcVal = self.player.calcpoints()
        #ensure the province is counted
        self.assertEqual(funcVal, 9)
        #add a garden to test the garden calculation (should be 1 point for 12 cards)
        self.player.deck.append(Dominion.Gardens())
        funcVal = self.player.calcpoints()
        #ensure the garden is counted (3 + 6 + 1)
        self.assertEqual(funcVal, 10)