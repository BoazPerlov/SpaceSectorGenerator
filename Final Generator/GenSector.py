import numpy as np
import pandas as pd
from random import randint
from math import floor
import sqlite3

dfSpace = pd.read_csv('Sector.csv')
dfStars = pd.read_csv('Star System.csv')
dfTrade = pd.read_csv('Trade Hub.csv')
dfShips = pd.read_csv('Ships.csv')
dfFactions = pd.read_csv('sFactions.csv')

planetHex = []
factionHex = []
shipHex = []
data = []
sectorHex = ["A1", "A3", "A5", "A7", "A9", "A11", "A13", "A15", "B2", "B4", "B6", "B8", "B10", "B12", "B14", "C1", "C3", "C5", "C7", "C9", "C11", "C13", "C15", "D2", "D4", "D6", "D8", "D10", "D12", 
			"D14", "E1", "E3", "E5", "E7", "E9", "E11", "E13", "E15", "F2", "F4", "F6", "F8", "F10", "F12", "F14", "G1", "G3", "G5", "G7", "G9", "G11", "G13", "G15", "H2", "H4", "H6", "H8", "H10", 
			"H12", "H14", "I1", "I3", "I5", "I7", "I9", "I11", "I13", "I15", "J2", "J4", "J6", "J8", "J10", "J12", "J14", "K1", "K3", "K5", "K7", "K9", "K11", "K13", "K15", "L2", "L4", "L6", "L8", 
			"L10", "L12", "L14", "M1", "M3", "M5", "M7", "M9", "M11", "M13", "M15", "N2", "N4", "N6", "N8", "N10", "N12", "N14", "O1", "O3", "O5", "O7", "O9", "O11", "O13", "O15", "P2", "P4", "P6", 
			"P8", "P10", "P12", "P14", "Q1", "Q3", "Q5", "Q7", "Q9", "Q11", "Q13", "Q15", "R2", "R4", "R6", "R8", "R10", "R12", "R14", "S1", "S3", "S5", "S7", "S9", "S11", "S13", "S15", "T2", "T4", 
			"T6", "T8", "T10", "T12", "T14", "U1", "U3", "U5", "U7", "U9", "U11", "U13", "U15", "V2", "V4", "V6", "V8", "V10", "V12", "V14", "W1", "W3", "W5", "W7", "W9", "W11", "W13", "W15", "X2", 
			"X4", "X6", "X8", "X10", "X12", "X14", "Y1", "Y3", "Y5", "Y7", "Y9", "Y11", "Y13", "Y15", "Z2", "Z4", "Z6", "Z8", "Z10", "Z12", "Z14", "Ω1", "Ω3", "Ω5", "Ω7", "Ω9", "Ω11", "Ω13", "Ω15"]
dfGeneratedSector = pd.DataFrame(data, index=sectorHex)
dfGeneratedTradeHub = pd.DataFrame(data)
dfGeneratedShips = pd.DataFrame(data)
dfGeneratedStarSystem = pd.DataFrame(data)
dfGeneratedFaction = pd.DataFrame(data)

starSystemNum = 0 #These are used to count the number of star systems, ships and factions in the sector
shipNum = 0
factionNum = 0

class shipFitting: 
	def __init__(self,cost,power,mass,minReqClass): #Class to represent various technologies which may be fitted on a starship
		self.cost = cost
		self.power = power
		self.mass = mass
		self.minReqClass = minReqClass

class starShip: #Class to represent starship
	def __init__(self, cost, speed, armour, hp, minCrew, maxCrew, ac, power, mass, hardPoints, shipClass):
		self.cost = cost
		self.speed = speed
		self.armour = armour
		self.hp = hp
		self.minCrew = minCrew
		self.maxCrew = maxCrew
		self.ac = ac
		self.power = power
		self.mass = mass
		self.hardPoints = hardPoints
		self.shipClass = shipClass #Fighter = 1, Frigate = 2, Cruiser = 3, Capital = 4

class shipDefences: #Why is this not an instance of shipFitting? TODO to look into it
	def __init__(self,cost,power,mass,minReqClass):
		self.cost = cost
		self.power = power
		self.mass = mass
		self.minReqClass = minReqClass

class shipWeapons: #Why is this not an instance of shipFitting? TODO to look into it
	def __init__(self, cost, dmg, power, mass, hardPoints, minReqClass):
		self.cost = cost
		self.dmg = dmg
		self.power = power
		self.mass = mass
		self.hardPoints = hardPoints
		self.minReqClass = minReqClass

class faction: #Faction class
	def __init__(self,type,alignment,hp, forceRating, cunningRating, wealthRating, facCreds, xp, homewolrld,tags, goals, assets):
		self.type = type
		self.alignment = alignment
		self.hp = hp
		self.forceRating = forceRating
		self.cunningRating = cunningRating
		self.wealthRating = wealthRating
		self.facCreds = facCreds
		self.xp = xp
		self.homewolrld = homewolrld
		self.tags = tags
		self.goals = goals
		self.assets = assets

shipsDict = {"Strike Fighter":starShip(200000,5,5,8,1,1,16,5,2,1, 1),
			"Shuttle":starShip(200000,3,0,15,1,10,11,3,5,1, 1),
			"Free Merchant":starShip(500000,3,2,20,1,6,14,10,15,2, 2),
			"Patrol Boat":starShip(25000000,4,5,25,5,20,14,15,10,4,2), 
			"Corvette":starShip(4000000,2,10,40,10,40,13,15,15,6,2), 
			"Heavy Frigate":starShip(7000000,1,10,50,30,120,15,25,20,8,2),
			"Bulk Freighter":starShip(5000000,0,0,40,10,40,13,15,15,6,3), 
			"Fleet Cruiser":starShip(10000000,1,15,60,50,200,14,50,30,10,3), 
			"Battleship":starShip(50000000,0,20,100,200,1000,16,75,50,15, 4),
			"Carrier":starShip(60000000,0,10,75,300,1500,14,50,100,4,4)
			}

fittingsDict= {"Advanced Lab":shipFitting(10000,1,2,2),
			"Advanced Nav Computer":shipFitting(10000,1,0,2),
		    "Amphibious operation":shipFitting(25000,1,1,1),
		    "Armory":shipFitting(10000,0,0,2),
		    "Atmosphere Configuration":shipFitting(5000,0,1,1),
		    "Auto Targeting System":shipFitting(50000,1,0,1),
		    "Automation Support":shipFitting(10000,2,1,1),
		    "Boarding Tubes":shipFitting(5000,0,1,2),
		    "Cargo Lighter":shipFitting(25000,0,2,2),
		    "Cargo Space":shipFitting(0,0,1,1),
		    "Cold Sleep Pods":shipFitting(5000,1,1,2),
		    "Colony Core":shipFitting(100000,4,2,2),
		    "Hyperspace Course Regulator":shipFitting(25000,1,1,2),
		    "Jump Engine":shipFitting(100000,3,3,2),
		    "Drop Pod":shipFitting(300000,0,2,2),
		    "Emissions Dampers":shipFitting(25000,1,1,1),
		    "Exodus Bay":shipFitting(25000,1,1,1),
		    "Extended Life Support":shipFitting(5000,1,1,1),
		    "Extended Medbay":shipFitting(5000,1,1,2),
		    "Extended Stores":shipFitting(2500,0,1,1),
		    "Fuel Bunkers":shipFitting(2500,0,1,1),
		    "Fuel Scoops":shipFitting(5000,2,1,2),
		    "Hydrophonic Production":shipFitting(10000,1,2,3),
		    "Lifeboats":shipFitting(5000,2,1,2),
		    "Luxury Cabins":shipFitting(10000,1,1,2),
		    "Mobile Extractor":shipFitting(50000,3,2,3),
		    "Precognitive Nav Chamber":shipFitting(100000,1,0,2),
		    "Psionic Anchorpoint":shipFitting("Special",3,0,2),
		    "Sensor Mask":shipFitting(10000,1,0,2),
		    "Ship Bay/Fighter":shipFitting(200000,0,2,3),
		    "Ship Bay/Frigate":shipFitting(1000000,1,4,4),
		    "Ship's Locker":shipFitting(2000,0,0,2),
		    "Shiptender Mount":shipFitting(25000,1,1,2),
		    "Smuggler's Hold":shipFitting(2500,0,1,1),
		    "Survey Sensor Array":shipFitting(5000,2,1,2),
		    "Teleportation pads":shipFitting("Special",1,1,2),
		    "Tractor Beams":shipFitting(10000,2,1,2),
		    "Vehicle Transport Fittings":shipFitting(2500,0,1,2),
		    "Workshop":shipFitting(500,1,0.5,2),
		    "Ablative Hull Compartments":shipDefences(100000,5,2,4),
			"Augmented Plating":shipDefences(25000,0,1,1),
			"Boarding Countermeasures":shipDefences(25000,2,1,2),
			"Burst ECM Generator":shipDefences(25000,2,1,2),
			"Foxer Drones":shipDefences(10000,2,1,3),
			"Grav Eddy Displacer":shipDefences(50000,5,2,2),
			"Hardened Polyceramic Overlay":shipDefences(25000,0,1,1),
			"Planetary Defense Array":shipDefences(50000,4,2,2),
			"Point Defense Lasers":shipDefences(10000,3,2,2),
			"Multifocal Laser":shipWeapons(100000,"1d4",5,1,1,1),
			"Reaper Battery":shipWeapons(100000,"3d4",4,1,1,1),
			"Fractal Impact Charge":shipWeapons(200000,"2d6",5,1,1,1),
			"Polyspectral MES Beam":shipWeapons(2000000,"2d4",3,1,1,1),
			"Sandthrower":shipWeapons(50000,"2d4",3,1,1,1),
			"Flak Emitter Battery":shipWeapons(500000,"2d6",5,3,1,2),
			"Torpedo Launcher":shipWeapons(500000,"3d8",10,3,1,2),
			"Charged Particle Caster":shipWeapons(800000,"3d6",10,1,2,2),
			"Plasma Beam":shipWeapons(700000,"3d6",5,2,2,2),
			"Mag Spike Array":shipWeapons(1000000,"2d6+2",5,2,2,2),
			"Nuclear Missiles":shipWeapons(50000,"Special",5,1,2,2),
			"Spinal Beam Cannon":shipWeapons(15000000,"3d10",10,5,3,3),
			"Smart Cloud":shipWeapons(2000000,"3d10",10,5,2,3),
			"Gravcannon":shipWeapons(2000000,"4d6",15,4,3,3),
			"Jump Inversion Projector":shipWeapons(2500000,"3d8",10,3,3,3),
			"Vortex Tunnder Inductor":shipWeapons(5000000,"3d20",20,10,4,4),
			"Mass Cannon":shipWeapons(5000000,"2d20",10,5,4,4),
			"Lightning Charge Mantle":shipWeapons(4000000,"1d20",15,5,2,4),
			"Singularity Gun":shipWeapons(200000000,"5d20",25,10,5,4)}

factionsDict = {}

def startPoint():
	max = len(sectorHex)
	rowName = dfGeneratedSector.index[randint(1,max)]
	colName = "Starting Point"
	dfGeneratedSector.loc[rowName,colName] = "STARTING POINT"

def generateShip(rowNum):
	fittingList = []
	for col in dfShips.columns:
		if col == "Ship Name" or col == "Origin":
			colTotal = dfShips[col].count()
			rowResult = randint(1,colTotal-1)
			dfGeneratedShips.at[rowNum,col] = dfShips.loc[rowResult,col]
			dfGeneratedShips.loc[rowNum,'Hex'] = shipHex[rowNum]
		elif col == "Hull Type":
			colTotal = dfShips[col].count()
			rowResult = randint(1,colTotal-1)
			hullType = dfShips.loc[rowResult,col]
			dfGeneratedShips.loc[rowNum,col] = dfShips.loc[rowResult,col]
			dfGeneratedShips.loc[rowNum,"Cost"] = shipsDict[hullType].cost
			dfGeneratedShips.loc[rowNum,"Speed"] = shipsDict[hullType].speed
			dfGeneratedShips.loc[rowNum,"Armour"] = shipsDict[hullType].armour
			dfGeneratedShips.loc[rowNum,"Health Points"] = shipsDict[hullType].hp
			dfGeneratedShips.loc[rowNum,"Minimal Crew"] = shipsDict[hullType].minCrew
			dfGeneratedShips.loc[rowNum,"Maximal Crew"] = shipsDict[hullType].maxCrew
			dfGeneratedShips.loc[rowNum,"Armour Class"] = shipsDict[hullType].ac
			dfGeneratedShips.loc[rowNum,"Power Rating"] = shipsDict[hullType].power
			dfGeneratedShips.loc[rowNum,"Mass Rating"] = shipsDict[hullType].mass
			dfGeneratedShips.loc[rowNum,"Hard Points"] = shipsDict[hullType].hardPoints
			dfGeneratedShips.loc[rowNum,"Ship Class"] = shipsDict[hullType].shipClass
		elif col == "Fittings":
			while True:
				colTotal = dfShips[col].count()
				rowResult = randint(1,colTotal-1)
				powerRating = 0
				massRating = 0
				hardPointRating = 0
				for i in range(len(fittingList)):
					if fittingsDict[fittingList[i]].minReqClass <= shipsDict[hullType].shipClass:
						powerRating = (powerRating + (fittingsDict[fittingList[i]].power))*shipsDict[hullType].shipClass
						massRating = (massRating + (fittingsDict[fittingList[i]].mass))*shipsDict[hullType].shipClass
						if hasattr(fittingsDict[fittingList[i]], 'hardPoints'):
							hardPointRating += fittingsDict[fittingList[i]].hardPoints
				if shipsDict[hullType].shipClass == 1:
					maxFittings = randint(1,3)
					for i in range(maxFittings):
						rowResult = randint(1,colTotal-1)
						fittingList.append(dfShips.loc[rowResult,col])
					break
				elif powerRating <= shipsDict[hullType].power and massRating <= shipsDict[hullType].mass and hardPointRating <= shipsDict[hullType].hardPoints:
					fittingList.append(dfShips.loc[rowResult,col])
					randomInteger = randint(1,10)
					if randomInteger > 7 and shipsDict[hullType].shipClass < 3:
						break
					else:
						continue
				else:
					break
			dfGeneratedShips.loc[rowNum,"Fittings"] = ', '.join(fittingList)
	randNum = randint(-2,4)
	randNum = roll_2d6() + randNum - floor(dfGeneratedShips.loc[rowNum,"Ship Class"]/2)
	if randNum < 6:
		dfGeneratedShips.loc[rowNum,"Detection Difficulty"] = "Auto Detection"
	else:
		dfGeneratedShips.loc[rowNum,"Detection Difficulty"] = randNum

def tradeHub(rowNum):
	mod = randint(1,10)
	#for i in range(1,5):
	for colName in dfGeneratedSector.columns:
		#colName = "Encounter #" + str(i)
		rowValue = dfGeneratedSector.loc[rowNum,colName]
		if pd.notnull(dfGeneratedSector.loc[rowNum,colName]):
			if "Ship Sighting:" in rowValue:
				mod += 0.5
			if "Star System" in rowValue:
				mod += 1
			if "Derelict" in rowValue:
				mod -=1
			if "Wormhole" in rowValue:
				mod += 2
	if mod >= 10:
		dfGeneratedSector.loc[rowNum,'Trade Hub'] = "Yes"
		for col in dfTrade.columns:
			colTotal = dfTrade[col].count()
			rowResult = randint(1,colTotal-1)
			dfGeneratedTradeHub.at[rowNum,col] = dfTrade.loc[rowResult,col]

def roll_2d6():
    num1 = randint(1,6)
    num2 = randint(1,6)
    return num1 + num2

def encounter(hex):
	for i in range(1,5):
		result = roll_2d6()
		if result == 2:
			colTotal = dfSpace['Aphiri Patrol'].count()
			rowResult = randint(1,colTotal)-1
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Aphiri Patrol: " + str(dfSpace.loc[rowResult,'Aphiri Patrol'])
		elif result >= 3 and result <=4:
			colTotal = dfSpace['Anomaly'].count()
			rowResult = randint(1,colTotal)-1
			colName = "Encounter #" + str(i)
			randNum = randint(-2,4)
			randNum = roll_2d6() + randNum
			if randNum < 6:
				dfGeneratedSector.loc[hex,colName] = "Anomaly: " + str(dfSpace.loc[rowResult,'Anomaly'] + " Detection skill difficulty check: Auto Detection")
			else:
				dfGeneratedSector.loc[hex,colName] = "Anomaly: " + str(dfSpace.loc[rowResult,'Anomaly'] + " Detection skill difficulty check: " + str(randNum))
		elif result >= 5 and result <=6:
			colTotal = dfSpace['Ship Encounter'].count()
			rowResult = randint(1,colTotal)-1
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Ship Sighting: " + str(dfSpace.loc[rowResult,'Ship Encounter'])
			global shipNum 
			shipNum += 1
			shipHex.append(hex)
		elif result >= 7 and result <=8:
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Nothing"
		elif result >=9 and result <=10:
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Star System"
			global starSystemNum 
			starSystemNum+=1
			planetHex.append(hex)
			isThereFactionHere = randint(1,100)
			if isThereFactionHere >= 95:
				global factionNum
				factionNum += 1
				factionHex.append(hex)
		elif result == 11:
			colTotal = dfSpace['Distress Beacon'].count()
			rowResult = randint(1,colTotal)-1
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Distress Beacon: " + str(dfSpace.loc[rowResult,'Distress Beacon'])
		elif result == 12:
			colTotal = dfSpace['Ship Malfunction'].count()
			rowResult = randint(1,colTotal)-1
			colName = "Encounter #" + str(i)
			dfGeneratedSector.loc[hex,colName] = "Ship Malfunctoin: " + str(dfSpace.loc[rowResult,'Ship Malfunction'])
	tradeHub(hex)

def jumpGate(rowNum):
	result = randint(1,10)
	mod = 0
	if dfStars.loc[rowNum,'Tech level'] == "Current technology":
		mod = mod + 1
	if dfStars.loc[rowNum,'Tech level'] == "Super advanced tech":
		mod = mod + 2
	if dfStars.loc[rowNum,'Tech level'] == "Medieval technology" or dfStars.loc[rowNum,'Tech level'] == "Stone age technology":
		mod = mod - 1
	if dfStars.loc[rowNum,'Population size'] == "Failed Colony" :
		mod = mod - 1
	if dfStars.loc[rowNum,'Star type'] == "Black hole" :
		mod = mod - 1
	if dfStars.loc[rowNum,'Population size'] == "Millions":
		mod = mod + 1 
	if dfStars.loc[rowNum,'Population size'] == "Billions":
		mod = mod + 2
	if dfStars.loc[rowNum,'Planet-side locales and hooks'] == "Major Shipyard":
		mod = mod + 2

	result = result + mod
	if result == 9 or result == 10:
		jumpGateStatus = randint(1,10)
		if jumpGateStatus == 1:
			dfGeneratedStarSystem.loc[rowNum,'Jump Gate'] = 2 #Faulty Jump Gate present
		else:
			dfGeneratedStarSystem.loc[rowNum,'Jump Gate'] = 1 #Jump Gate present
	else:
		dfGeneratedStarSystem.loc[rowNum,'Jump Gate'] = 0 #No Jump Gate present

def planetGenerator(rowNum):
	for col in dfStars.columns:
		Tags = ""
		if col == 'World Tags':
			for i in range(3):
				colTotal = dfStars[col].count()
				rowResult = randint(1,colTotal-1)
				if i ==2:
					Tags = Tags + dfStars.loc[rowResult,col]
				else:
					Tags = Tags + dfStars.loc[rowResult,col] +  ", "
			dfGeneratedStarSystem.loc[rowNum,col] = Tags
			dfGeneratedStarSystem.loc[rowNum,'Hex'] = planetHex[rowNum]
		elif col == "Planet-side locales and hooks":
			for i in range(3):
				colTotal = dfStars[col].count()
				rowResult = randint(1,colTotal-1)
				if i == 2:
					Tags = Tags + dfStars.loc[rowResult,col]
				else:
					Tags = Tags + dfStars.loc[rowResult,col] +  ", "
			dfGeneratedStarSystem.loc[rowNum,col] = Tags
			dfGeneratedStarSystem.loc[rowNum,'Hex'] = planetHex[rowNum]
		elif col == "Planet Tilt":
			degree_sign = u"\N{DEGREE SIGN}"
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			if dfStars.loc[rowResult,col] == 1:
				dfGeneratedStarSystem.at[rowNum,col] = "0" + degree_sign
			else:
				tilt = randint(1,10)
				mod = (int(dfStars.loc[rowResult,col]) - 2)*10
				dfGeneratedStarSystem.at[rowNum,col] = str(tilt+mod) + degree_sign
		elif col == "Hours Per Day":
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			dfGeneratedStarSystem.at[rowNum,col] = int(dfStars.loc[rowResult,col]) * rowResult
		elif col == "Hydrosphere":
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			if rowResult == 1:
				dfGeneratedStarSystem.at[rowNum,col] = "0%" 
			elif rowResult == 2:
				dfGeneratedStarSystem.at[rowNum,col] = str(randint(1,5)) + "%"
			else:
				result = int(dfStars.loc[rowResult,col])
				hydros = randint(1,10) + result*5
				if hydros <= 100:
					dfGeneratedStarSystem.at[rowNum,col] = str(hydros) + "%"
				else:
					dfGeneratedStarSystem.at[rowNum,col] = "100%"
		elif col == "Population Breakdown":
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			if dfStars.loc[rowResult,col] == "Equal Parts" or dfStars.loc[rowResult,col] == "TechNet World":
				dfGeneratedStarSystem.at[rowNum,col] = dfStars.loc[rowResult,col]
			else:
				dfGeneratedStarSystem.at[rowNum,col] = "Predominantly " + dfStars.loc[rowResult,col]
		elif col == "System Name":
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			dfGeneratedStarSystem.loc[rowNum,'Hex'] = planetHex[rowNum]
			randNum = randint(1,100)
			if randNum > 98:
				dfGeneratedStarSystem.at[rowNum,col] = dfStars.loc[rowResult,col] + " Hegemony"
			elif randNum > 95:
				starsuffix = ["Prime", "V", "I", "II", "III", "IV", "VI", "VII", "Sigma", "XX", "Theta", "Primus", "Secundus", "Tertius", "Gamma", "Alpha", "Epsilon", "Omicron", "19"]
				randNum2 = randint(1,len(starsuffix)-1)
				dfGeneratedStarSystem.at[rowNum,col] = dfStars.loc[rowResult,col] + " " + starsuffix[randNum2]
			else:
				dfGeneratedStarSystem.at[rowNum,col] = dfStars.loc[rowResult,col]
		else:
			colTotal = dfStars[col].count()
			rowResult = randint(1,colTotal-1)
			dfGeneratedStarSystem.at[rowNum,col] = dfStars.loc[rowResult,col]
			jumpGate(rowNum)
			knownPlanet(rowNum)
	randNum = roll_2d6() - 1
	if randNum < 6:
		dfGeneratedStarSystem.loc[rowNum,"Detection Difficulty"] = "Auto Detection"
	else:
		dfGeneratedStarSystem.loc[rowNum,"Detection Difficulty"] = randNum

def factionGenerator(rowNum):
	for col in dfFactions.columns:
		colTotal = dfFactions[col].count()
		rowResult = randint(1,colTotal-1)
		dfGeneratedFaction.loc[rowNum,"Hex"] = factionHex[rowNum]
		dfGeneratedFaction.at[rowNum,col] = dfFactions.loc[rowResult,col]
		
def generateAll():
	for hex in sectorHex:
		encounter(hex)
	for i in range(starSystemNum):
		planetGenerator(i)
	for i in range(shipNum):
		generateShip(i)
	for i in range(factionNum):
		factionGenerator(i)

def checkIfFactionHomeworld():
	for i in range(starSystemNum):
		for j in range(factionNum):
			if planetHex[i] == factionHex[j]:
				dfGeneratedStarSystem.loc[i,"Faction Homeworld?"] = "Faction Base" #dfGeneratedFaction.loc[j,"Faction Name"]

def checkStarSystemName():
	names = []
	j = 0
	for i in range(starSystemNum):
		for hex in sectorHex:
			if planetHex[i] == hex:
				name = dfGeneratedStarSystem.loc[i,"System Name"]
				names.append(name)
				for col in dfGeneratedSector.columns:
					if dfGeneratedSector.loc[hex,col] == "Star System" and j < len(names):
						dfGeneratedSector.loc[hex,col] = dfGeneratedSector.loc[hex,col] + ": " + names[j]
						j +=1

def knownPlanet(rowNum):
	result = randint(1,10)
	mod = 0
	if dfStars.loc[rowNum,'Tech level'] == "Current technology":
		mod = mod + 1
	if dfStars.loc[rowNum,'Tech level'] == "Super advanced tech":
		mod = mod + 2
	if dfStars.loc[rowNum,'Tech level'] == "Medieval technology" or dfStars.loc[rowNum,'Tech level'] == "Stone age technology":
		mod = mod - 1
	if dfStars.loc[rowNum,'Population size'] == "Failed Colony" :
		mod = mod - 1
	if dfStars.loc[rowNum,'Star type'] == "Black hole" :
		mod = mod - 1
	if dfStars.loc[rowNum,'Population size'] == "Millions":
		mod = mod + 1 
	if dfStars.loc[rowNum,'Population size'] == "Billions":
		mod = mod + 2
	if dfStars.loc[rowNum,'Planet-side locales and hooks'] == "Major Shipyard":
		mod = mod + 2
	result = result + mod
	if result == 9 or result == 10:
		dfGeneratedStarSystem.loc[rowNum,'System Reputation'] = 2 #System Known throughout sector
	elif result == 7 or result == 8:
		dfGeneratedStarSystem.loc[rowNum,'System Reputation'] = 1 #System Known up to 5 hexes away
	else:
		dfGeneratedStarSystem.loc[rowNum,'System Reputation'] = 0 #System unknown, no major trade links 


generateAll()
startPoint()  
checkIfFactionHomeworld()
checkStarSystemName()

'''dfGeneratedStarSystem.to_csv("Generated Star Systems.csv", index=False, encoding = 'utf-8')
dfGeneratedSector.to_csv("Generated Sector.csv",index=True)
dfGeneratedTradeHub.to_csv("Genreated Trade Hub.csv",index=True)
dfGeneratedShips.to_csv("Generated Ships.csv", index=False)
dfGeneratedFaction.to_csv("Generated Factions.csv", index = False)'''

sectorDB = sqlite3.connect('C:/Users/Boazp/OneDrive/Documents/SPAAAACE/Final Generator/GeneratedDB/sector.db')
shipsDB = sqlite3.connect('C:/Users/Boazp/OneDrive/Documents/SPAAAACE/Final Generator/GeneratedDB/ships.db')
tradeHubDB = sqlite3.connect('C:/Users/Boazp/OneDrive/Documents/SPAAAACE/Final Generator/GeneratedDB/tradeHub.db')
starSystemsDB = sqlite3.connect('C:/Users/Boazp/OneDrive/Documents/SPAAAACE/Final Generator/GeneratedDB/starSystems.db')

dfGeneratedSector.to_sql('Sector', sectorDB, if_exists='replace')
dfGeneratedStarSystem.to_sql('Star Systems', starSystemsDB, if_exists='replace')
dfGeneratedTradeHub.to_sql('Trade Hubs', tradeHubDB, if_exists='replace')
dfGeneratedShips.to_sql('Ships', shipsDB, if_exists='replace')

with pd.ExcelWriter('Final Generated Sector.xlsx') as writer:
	dfGeneratedSector.to_excel(writer, sheet_name='Sector')
	dfGeneratedStarSystem.to_excel(writer, sheet_name='Star Systems', index=False)
	dfGeneratedShips.to_excel(writer, sheet_name='Ships', index=False)
	dfGeneratedTradeHub.to_excel(writer, sheet_name='Trade Hubs')
	#dfGeneratedFaction.to_excel(writer, sheet_name='Factions', index=False)