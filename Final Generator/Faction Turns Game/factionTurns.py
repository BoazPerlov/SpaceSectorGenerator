'''
Goals:
1. create a dataframe of possible factions + their traits
2. generate a dataframe of factions, based on randomness and specfici trait rules
3. Set up a factions class
4. Create a list of faction objects
5. Set up turns
6. Output end result

'''
import math
import randomdict
from randomdict import RandomDict
from random import randint
import random
import pandas as pd
import numpy as np
from Roller import diceRoller
import os
import sys

class Faction():
	def __init__(self,homeworld=None,name=None,facType=None, mainSpec=None, tags=None, goals=None, assets=None,hp=None,fRating=None,cRating=None,wRating=None,
				 relationship=None,legal=None,xp=None,facCreds=0):
		self.name = name
		self.facType = facType
		self.relationship = relationship
		self.mainSpec = mainSpec
		self.hp = hp
		self.fRating = fRating
		self.cRating = cRating
		self.wRating = wRating
		self.facCreds = facCreds
		self.xp = xp
		self.homeworld = homeworld
		self.tags = tags
		self.goals = goals
		self.assets = assets
		self.legal = legal
		self.assets = []

	def calcStats(self): 
		#calculate faction ratings (force, cunning, wealth). Each has primary, secondary and tertiary stats.
		#Primary = 1d6+2. Secondary = 1d6. Tertiary = 1d6-2
		randnum = randint(1,3)
		if randnum == 1:
			#force faction
			self.mainSpec = "Force"
			self.fRating = randint(2,6)+2
			randBool = random.choice([True, False])
			if randBool:
				self.cRating = randint(3,6)-2
				self.wRating = randint(1,6)
			else:
				self.wRating = randint(3,6)-2
				self.cRating = randint(1,6)
		elif randnum == 2:
			#cunning faction
			self.mainSpec = "Cunning"
			self.cRating = randint(2,6)+2
			randBool = random.choice([True, False])
			if randBool:
				self.fRating = randint(3,6)-2
				self.wRating = randint(1,6)
			else:
				self.wRating = randint(3,6)-2
				self.fRating = randint(1,6)
		elif randnum == 3:
			#wealth faction
			self.mainSpec = "Wealth"
			self.wRating = randint(2,6)+2
			randBool = random.choice([True, False])
			if randBool:
				self.cRating = randint(3,6)-2
				self.fRating = randint(1,6)
			else:
				self.fRating = randint(3,6)-2
				self.cRating = randint(1,6)
		self.tags = random.choice(["Colonists", "Deep Rooted", "Eugenics Cult", "Exchange Consulate", "Fanatical", "Imperialists", "Machiavellian", 
						"Mercenary Group", "Perimeter Agency", "Pirates", "Planetary Government", "Plutocratic", "Pereceptor Archive", "Psychic Academy", 
						"Warlike", "Theocratic", "Technical Expertise", "Secretive", "Scavengers", "Savage"])
		self.facType = random.choice(["Regional Hegemon", "Eugenics Cult", "Criminal Org", "TechNet faction", "Glorious Evolotion Proponents", "Refugee Flotila", 
						"Shadow Broker", "Zealous Faith", "Hivemind", "Military Hegemony", "Mercanary Group", "Rebel Freedom Fighters", "Systems Alliance", 
						"Mercantile Combine", "Teamsters", "Science Corp", "Indsutry Corp", "Religious Group"])
		self.name = random.choice(["Starlight", "The Black Company", "Stellaris Global Industries", "Meakin Co.", "Harkana Group", "Z9XRAV5", "Hellarion", 
						"Orbfire", "RTI inc.", "Elan Megacorp", "Coralline Family", "The Defiance", "Plutcondia Combine", "New Africo"])
		randRelationship = randint(1,3)
		randLegal = randint(1,3)
		leg = {1:'Criminal',2:'Neutral',3:'Lawful'}
		rel = {1:'Hostile',2:'Neutral',3:'Friendly'}
		self.relationship=rel[randRelationship]
		self.legal = leg[randLegal]

	def calcHP(self):
		hpValueDict = {1:1,2:2,3:4,4:6,5:9,6:12,7:16,8:20}
		self.hp = 4 + hpValueDict[self.fRating] + hpValueDict[self.cRating] + hpValueDict[self.wRating]

	def calcFacCreds(self):
		self.facCreds = self.facCreds + math.ceil(self.wRating/2) + math.floor((self.fRating+self.cRating)/4)

	def startAsset(self):
		while True:
			if self.mainSpec == 'Cunning':
				asset = cunningAssetsDict.random_key()
				if cunningAssetsDict[asset].rating <= self.cRating and cunningAssetsDict[asset].cost <= self.facCreds:
					self.assets.insert(0,asset)
					break
			elif self.mainSpec == 'Force':
				asset = forceAssetsDict.random_key()
				if forceAssetsDict[asset].rating <= self.fRating  and forceAssetsDict[asset].cost <= self.facCreds:
					self.assets.insert(0,asset)
					break
			elif self.mainSpec == 'Wealth':
				asset = wealthAssetsDict.random_key()
				if wealthAssetsDict[asset].rating <= self.wRating and wealthAssetsDict[asset].cost <= self.facCreds:
					self.assets.insert(0,asset)
					break

class Asset():
	def __init__(self,assetType,rating,hp,cost,description,attckVS=None,damage=None):
		self.assetType = assetType
		self.rating = rating
		self.hp = hp
		self.cost = cost
		self.description = description
		self.attckVS = attckVS
		self.damage = damage

class Action():
	def __init__(self,actionLegal, actionRel):
		self.actionLegal = actionLegal
		self.actionRel = actionRel		

cunningAssetsDict = RandomDict({
	'Smugglers':Asset('Cunning',1,4,2,'Starship','Wealth',diceRoller(1,4)),
	'Informers':Asset('Cunning',1,3,2,'Special Forces','Cunning','Special'),
	'False Front':Asset('Cunning',1,2,1,'Logistics Facility'),
	'Lobbyists':Asset('Cunning',2,4,4,'Special Forces','Cunning','Special'),
	'Saboteurs':Asset('Cunning',2,6,5,'Special Forces','Cunning',diceRoller(2,4)),
	'Blackmail':Asset('Cunning',2,4,4,'Tactic','Cunning',(diceRoller(1,4)+1)),
	'Seductress':Asset('Cunning',2,4,4,'Special Forces','Cunning','Special'),
	'Cyberninjas':Asset('Cunning',3,4,5,'Special Forces','Cunning',diceRoller(2,6)),
	'Stealth':Asset('Cunning',3,0,2,'Tactic'),
	'Covert Shipping':Asset('Cunning',3,4,8,'Logistics Facility'),
	'Party Machine':Asset('Cunning',4,10,8,'Logistics Facility','Cunning',diceRoller(2,6)),
	'Vangaurd Cadres':Asset('Cunning',4,12,'Military Unit','Cunning',diceRoller(1,6)),
	'Tripwire Cells':Asset('Cunning',4,8,12,'Special Forces'),
	'Seditionists':Asset('Cunning',4,8,12,'Special Forces'),
	'Organization Moles':Asset('Cunning',5,8,10,'Tactic','Cunning',diceRoller(2,6)),
	'Cracked Comms':Asset('Cunning',5,6,14,'Tactic'),
	'Boltholes':Asset('Cunning',5,6,12,'Logistics Facility'),
	'Transport Lockdown':Asset('Cunning',6,10,20,'Tactic','Cunning','Special'),
	'Covert Transit Net':Asset('Cunning',6,15,18,'Logistics Facility'),
	'Demagogue':Asset('Cunning',6,10,20,'Special Forces','Cunning',diceRoller(1,8)),
	'Popular Movement':Asset('Cunning',7,16,25,'Tactic','Cunning',diceRoller(2,6)),
	'Book of Secrets':Asset('Cunning',7,10,20,'Tactic'),
	'Treachery':Asset('Cunning',7,5,10,'Tactic','Cunning','Special'),
	'Panopticon Matrix':Asset('Cunning',8,20,30,'Logistics Facility')
})

forceAssetsDict = RandomDict({
	'Security Personnel':Asset('Force',1,3,2,'Military Unit','Force','1d3+1'),
	'Hitmen':Asset('Force',1,1,2,'Special Forces','Cunning','1d6'),
	'Militia Unit':Asset('Force',1,4,4,'Military Unit','Force','1d6'),
	'Heavy Drop Assets':Asset('Force',2,6,4,'Facility'),
	'Elite Skirmishers':Asset('Force',2,5,5,'Military Unit','Force','2d4'),
	'Hardened Personnel':Asset('Force',2,4,4,'Special Forces'),
	'Guerrilla Populace':Asset('Force',2,6,4,'Military Unit','Cunning',(diceRoller(1,4)+1)),
	'Zealots':Asset('Force',3,4,6,'Special Forces','Force',diceRoller(2,6)),
	'Cunning Trap':Asset('Force',3,2,5,'Tactic'),
	'Counterintel Unit':Asset('Force',3,4,6,'Special Forces','Cunning',(diceRoller(1,4)+1)),
	'Beachhead Landers':Asset('Force',4,10,10,'Facility'),
	'Extended Theater':Asset('Force',4,10,10,'Facility'),
	'Strike Fleet':Asset('Force',4,8,12,'Starship','Force',diceRoller(2,6)),
	'Infantry':Asset('Force',4,12,8,'Military Unit','Force',diceRoller(1,8)),
	'Blockade Fleet':Asset('Force',5,8,10,'Starship','Wealth',diceRoller(1,6)),
	'Pretech Logistics':Asset('Force',5,6,14,'Facility'),
	'Psychic Assassins':Asset('Force',5,4,12,'Special Forces','Cunning',(diceRoller(2,6)+2)),
	'Pretech Infantry':Asset('Force',6,16,20,'Military Unit','Force',diceRoller(2,8)),
	'Planetary Defenses':Asset('Force',6,20,18,'Facility'),
	'Gravtank Formation':Asset('Force',6,14,25,'Military Unit','Force',(diceRoller(2,10)+4)),
	'Deep Strike Landers':Asset('Force',7,10,25,'Facility'),
	'Integral Protocols':Asset('Force',7,10,20,'Facility'),
	'Space Marines':Asset('Force',7,16,30,'Military Unit','Force',(diceRoller(2,8)+2)),
	'Capital Fleet':Asset('Force',8,30,40,'Spaceship','Force',(diceRoller(3,10))),
	})

wealthAssetsDict = RandomDict({
	'Franchise':Asset('Wealth',1,3,2,'Facility','Wealth',diceRoller(1,4)),
	'Harvesters':Asset('Wealth',1,4,2,'Facility'),
	'Local Investments':Asset('Wealth',1,2,1,'Facility','Facility',(diceRoller(1,4)-1)),
	'Freighter Contract':Asset('Wealth',2,4,5,'Starship','Wealth',diceRoller(1,4)),
	'Lawyers':Asset('Wealth',2,4,6,'Special Forces','Wealth',diceRoller(2,4)),
	'Union Toughs':Asset('Wealth',2,6,4,'Military Unit','Force,',(diceRoller(1,4)+1)),
	'Surveyors':Asset('Wealth',2,4,4,'Special Forces'),
	'Postech Industry':Asset('Wealth',3,4,8,'Facility'),
	'Laboratory':Asset('Wealth',3,4,6,'Facility'),
	'Mercenaries':Asset('Wealth',3,6,8,'Military Unit','Force',(diceRoller(2,4)+2)),
	'Shipping Combine':Asset('Wealth',4,10,10,'Facility'),
	'Monopoly':Asset('Wealth',4,12,8,'Facility','Wealth',diceRoller(1,6)),
	'Medical Center':Asset('Wealth',4,8,12,'Facility'),
	'Bank':Asset('Wealth',4,8,12,'Facility'),
	'Marketers':Asset('Wealth',5,8,10,'Tactic','Wealth',diceRoller(1,6)),
	'Pretech Researchers':Asset('Wealth',5,6,14,'Special Forces'),
	'Blockade Runners':Asset('Wealth',5,6,12,'Starship'),
	'Venture Capital':Asset('Wealth',6,10,15,'Facility','Wealth',diceRoller(2,6)),
	'R&D Department':Asset('Wealth',6,15,18,'Facility'),
	'Commodities Broker':Asset('Wealth',6,10,20,'Special Forces','Wealth',diceRoller(2,8)),
	'Pretech Manufactory':Asset('Wealth',7,16,25,'Facility'),
	'Hostile Takeover':Asset('Wealth',7,10,20,'Tactic','Wealth',diceRoller(2,10)),
	'Transit Web':Asset('Wealth',7,5,15,'Facility','Cunning',diceRoller(1,12)),
	'Scavenger Fleet':Asset('Wealth',8,20,30,'Starship','Wealth',(diceRoller(2,10)+4))
	})

actionsDict = {
	'Attack':Action(1,1),
	'Buy Asset':Action(2,2),
	'Change Homeworld':Action(2,3),
	'Expand Influence':Action(3,1),
	'Refit Asset':Action(2,2),
	'Repair Asset':Action(2,2),
	'Sell Asset':Action(3,1),
	'Seize Planet':Action(2,1),
	'Use Asset Ability':Action(2,2)
}

data = []
dfGeneratedFaction = pd.DataFrame(data)
dfFactions = pd.read_csv('C:/Users/Boazp/OneDrive/Documents/SPAAAACE/Final Generator/Faction Turns Game/Factions.csv')


def factionGenerator(rowNum):
	for col in dfFactions.columns:
		colTotal = dfFactions[col].count()
		rowResult = randint(1,colTotal-1)
		dfGeneratedFaction.at[rowNum,col] = dfFactions.loc[rowResult,col]

def createFactionList(factionNumber):
	global facList
	facList = [Faction(i) for i in range(factionNumber)]
	for i in range(len(facList)):
		facList[i].calcStats()
		facList[i].calcHP()
		facList[i].calcFacCreds()
		facList[i].startAsset()

	for i in range(len(facList)):
		j = i + 1
		print(f'Faction #{j} is {facList[i].name}. It is a {facList[i].facType} specializing in {facList[i].mainSpec}')
		print(f"Its assets include {facList[i].assets}")
	turn(facList)

def turn(factionList):
	for i in range(len(facList)):
		turnsCounter = 1
		while turnsCounter <= 12:
			facList[i].calcFacCreds()
			facList[i].calcHP()
			print(f'At the start of turn number {turnsCounter}, {facList[i].name} has {facList[i].facCreds} credits and {facList[i].hp} hp')
			turnsCounter += 1


createFactionList(3)

#dfGeneratedFaction.to_csv("Generated Factions dsTEST.csv", index = False)
