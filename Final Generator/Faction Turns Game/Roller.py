from random import randint

def diceRoller(diceNum,diceSize):
	result = 0
	for i in range(diceNum):
		result =+ result + randint(1,diceSize)
	return result


