"""
Must be in same directory as glove.6B.50d.txt (inside glove.6B.zip downloaded from http://nlp.stanford.edu/projects/glove/)
and graphAttributes.txt

This script will automatically read in the files mentioned above to populate wordVecDict and userWordVecs, which
are GLOBAL variables
(adds ~20 seconds at the beginning)
"""

import Stemmer
import numpy as np

stemmer = Stemmer.Stemmer('english')
wordVecDict = {} # english word -> word vector
userWordVecs = {} # user id -> word vector (weighted average of all the word vectors used in the user's reviews)

def getCosSim(uid1, uid2):
	if not uid1 in userWordVecs or not uid2 in userWordVecs:
		print "ERROR: either uid1 or uid2 not in dict"
		return
	v1 = userWordVecs[uid1]
	v2 = userWordVecs[uid2]
	num = np.dot(v1, v2)
	denom = np.linalg.norm(v1) * np.linalg.norm(v2)
	return num / denom

def average(vecs):
	numVecs = len(vecs)
	if numVecs == 0:
		print "ERROR: No vectors in array"
		return
	sumArr = vecs[0]
	for i in xrange(1, len(vecs)):
		sumArr = np.add(sumArr, vecs[i])
	return np.divide(sumArr, numVecs)

def getUserWordVecs():
	global wordVecDict, userWordVecs
	with open('graphAttributesEdinburgh.txt') as f:
		for line in f:
			split = line.split('|')
			userid = split[0]
			reviewText = split[-1].split(',')
			wordVecs = []
			for i in xrange(0, len(reviewText) - 1, 2):
				if not reviewText[i] in wordVecDict: # we don't have the word vector associated with this word
					continue
				wordVec = wordVecDict[reviewText[i]]
				for j in xrange(0, int(reviewText[i + 1])): # add word the number of times it occurs
					wordVecs.append(wordVec)
			if userid in userWordVecs:
				userWordVecs[userid].extend(wordsVecs)
			else:
				userWordVecs[userid] = wordVecs

		for user in userWordVecs:
			userWordVecs[user] = average(userWordVecs[user])
		return userWordVecs

def createDict():
	global wordVecDict, stemmer
	with open('glove.6B.50d.txt') as f:
		for line in f:
			split = line.split(' ')
			key = stemmer.stemWord(split[0])
			wordVec = np.array([float(x) for x in split[1:]])
			if key in wordVecDict:
				wordVecDict[key].append(wordVec)
			else:
				wordVecDict[key] = [wordVec]
		
		for word in wordVecDict:
			wordVecDict[word] = average(wordVecDict[word])

		return wordVecDict

# LOAD DICTIONARIES FROM FILES
createDict()
print "Done creating word dict"
getUserWordVecs()
print "Done creating user word vectors"

if __name__ == "__main__":
	# EXAMPLE USAGE
	uid1 = 'VXbKx1v7MiwtYk6B9RhQ6g'
	uid2 = '4RU4zU3yDA3ewvrqE6kHLg'
	print(getCosSim(uid1, uid2))

