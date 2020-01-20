# -*- coding: utf-8 -*-
"""
Edited by Matthew Albrecht
Edited on 19 Jan 2020
"""

import testUtility
import Dominion
import random
from collections import defaultdict

#Get player names
player_names = testUtility.GetPlayernames()

#Get victory cards
nV = testUtility.GetVictory(player_names)
#force the number of victory cards to be 8, even if there are more than 2 players
nV = 8
#Get number of curses
nC = testUtility.GetCurses(player_names)

#Define box
box = testUtility.GetBoxes(nV)

#Get supply order
supply_order = testUtility.GetSupply()

#Pick 10 cards from box to be in the supply.
supply = testUtility.GetSupplyBox(box)

#Load Supply
testUtility.LoadSupply(supply, player_names, nV, nC)

#initialize the trash
trash = []

#Create Players
players = testUtility.CreatePlayers(player_names)

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)