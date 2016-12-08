import matplotlib.pyplot as plt
from dbHelper import *
import jaccard
import collections
import numpy as np

# calculatedSet = set()
# allJacSims = []
# print "Finding jaccard simularities between friends"
# with open("graphAttributes.txt", "r") as f:
# 	for line in f:
# 		split = line.split("|")
# 		user_id = split[0]
# 		friends = split[2].split(",")
# 		if (len(friends[0]) == 0): continue
# 		for user2 in friends:
# 			if (user_id, user2) not in calculatedSet:
# 				jacSim = jaccard.getJacSim(user_id, user2)
# 				if jacSim is not None:
# 					allJacSims.append(jacSim)
# 					calculatedSet.add((user_id, user2))
# 					calculatedSet.add((user2, user_id))
# plt.figure(1, facecolor='white')
# n, bins, patches = plt.hist(allJacSims)#, 50, normed=1)
# print "n"
# print n
# print ""
# print "bins"
# print bins
# plt.xlabel('Jaccard Similarities')
# plt.ylabel('Counts')
# plt.title('Jaccard Similarities of Friends')
# # plt.axis([0.6, 1.0, 0, 7000])
# plt.grid(True)
# plt.show()


numPairs = 0
randomPairs = set()
uids = set()
allJacSims = []
print "Finding jaccard simularities between friends"
with open("graphAttributes.txt", "r") as f:
	for line in f:
		split = line.split("|")
		user_id = split[0]
		friends = len(split[2].split(","))
		numPairs += friends
		uids.add(user_id)
	uids = list(uids)
	numPairs /= 2
	while len(randomPairs) < numPairs:
		randPair = np.random.choice(uids, 2, replace=False)
		while (randPair[0], randPair[1]) in randomPairs:
			randPair = np.random.choice(uids, 2, replace=False)
		jacSim = jaccard.getJacSim(randPair[0], randPair[1])
		if jacSim is not None:
			allJacSims.append(jacSim)
			randomPairs.add((randPair[0], randPair[1]))
			randomPairs.add((randPair[1], randPair[0]))
print "Done"
plt.figure(1, facecolor='white')
n, bins, patches = plt.hist(allJacSims, 30)
print "n"
print n
print ""
print "bins"
print bins
plt.xlabel('Jaccard Similarities')
plt.ylabel('Counts')
plt.title('Jaccard Similarities of Random Pairs')
# plt.axis([0.6, 1.0, 0, 7000])
plt.grid(True)
plt.show()