import matplotlib.pyplot as plt
from dbHelper import *
import wordVectorHelpers

calculatedSet = set()
allCosSims = []
print "Finding cosine simularities between friends"
with open("graphAttributes.txt", "r") as f:
	for line in f:
		split = line.split("|")
		user_id = split[0]
		friends = split[2].split(",")
		for user2 in friends:
			if (user_id, user2) not in calculatedSet:
				cosSim = wordVectorHelpers.getCosSim(user_id, user2)
				if cosSim is not None:
					allCosSims.append(cosSim)
					calculatedSet.add((user_id, user2))
					calculatedSet.add((user2, user_id))
plt.figure(1, facecolor='white')
n, bins, patches = plt.hist(allCosSims, 30)
print "n"
print n
print ""
print "bins"
print bins
plt.xlabel('Cosine Similarities')
plt.ylabel('Counts')
plt.title('Cosine Similarities of Friends')
# plt.axis([0.6, 1.0, 0, 7000])
plt.grid(True)
plt.show()