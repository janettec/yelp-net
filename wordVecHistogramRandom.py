import matplotlib.pyplot as plt
from dbHelper import *
import wordVectorHelpers
import numpy as np

numPairs = 0
randomPairs = set()
uids = set()
allCosSims = []
print "Finding cosine simularities between friends"
with open("graphAttributes.txt", "r") as f:
	for line in f:
		split = line.split("|")
		user_id = split[0]
		friends = len(split[2].split(","))
		numPairs += friends
		uids.add(user_id)
	uids = list(uids)
	while len(randomPairs) < numPairs:
		randPair = np.random.choice(uids, 2, replace=False)
		while (randPair[0], randPair[1]) in randomPairs:
			randPair = np.random.choice(uids, 2, replace=False)
		cosSim = wordVectorHelpers.getCosSim(randPair[0], randPair[1])
		if cosSim is not None:
			allCosSims.append(cosSim)
			randomPairs.add((randPair[0], randPair[1]))
			randomPairs.add((randPair[1], randPair[0]))
plt.figure(1, facecolor='white')
n, bins, patches = plt.hist(allCosSims, 30)
print "n"
print n
print ""
print "bins"
print bins
plt.xlabel('Cosine Similarities')
plt.ylabel('Counts')
plt.title('Cosine Similarities of Random Pairs')
# plt.axis([0.6, 1.0, 0, 7000])
plt.grid(True)
plt.show()