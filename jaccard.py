import numpy as np

userWordSets = {}

def getUserWordSets():
	global wordVecDict, userWordVecs
	with open('graphAttributes.txt') as f:
		for line in f:
			split = line.split('|')
			userid = split[0]
			reviewText = split[-1].split(',')
			words = set()
			for i in xrange(0, len(reviewText) - 1, 2):
				words.add(reviewText[i])
			userWordSets[userid] = words
print "Getting user word sets..."
getUserWordSets()
print "Done"

def getJacSim(uid1, uid2):
	wset1 = userWordSets[uid1]
	wset2 = userWordSets[uid2]
	return float(len(wset1 & wset2)) / float(len(wset1 | wset2))