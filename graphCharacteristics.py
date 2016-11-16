import snap
import dbHelper
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from sklearn import linear_model

def createFriendNetwork():
	userNetwork = snap.LoadEdgeList(snap.PUNGraph, "friend_edge_list.txt", 0, 1)
	noFriendUsers = dbHelper.selectUsers("ROWID", "user_id NOT IN (SELECT user1 FROM Friends)")
	for record in noFriendUsers:
		userNetwork.AddNode(int(record["ROWID"]))
	return userNetwork

def getPDF(xmin, xmax, alpha):
	xArr = range(xmin, xmax + 1)
	pArr = []
	for x in xArr:
		p = ((alpha - 1.0) / float(xmin)) * ((float(x) / float(xmin)) ** (-alpha))
		pArr.append(p)

	return pArr

def mleA(deg, nodes):
	denom = 0.0
	n = 0.0
	for i in xrange(0,len(deg)):
		denom += (math.log(deg[i])) * float(nodes[i])
		n += nodes[i]
	print n
	print "alpha from est MLE: %s" % str(1.0 + (float(n) / denom))
	return (1.0 + (float(n) / denom))

def plotDegDistr(G):
	DegToCntV = snap.TIntPrV()
	snap.GetDegCnt(G, DegToCntV)
	numNodes = G.GetNodes()
	print numNodes
	deg = []
	nodes = []
	tups = []
	for item in DegToCntV:
		if item.GetVal1() == 0:
			numNodes -= item.GetVal2()
			continue
		deg.append(item.GetVal1())
		nodes.append(item.GetVal2()) #float(item.GetVal2()) / float(numNodes))
		tups.append((item.GetVal1(), float(item.GetVal2())))
	pdf = []
	for tup in tups:
		pdf.append((tup[0], tup[1] / float(numNodes)))
	pdf.sort(key=lambda x: x[0])
	print pdf[:10]

	alpha = mleA(deg, nodes)
	estPDF = getPDF(pdf[1][0], pdf[-1][0], alpha)

	fig = plt.figure()
	ax = plt.gca()
	G1Dots, = ax.plot(deg , [float(x) / float(numNodes) for x in nodes], 'o', c='blue', alpha=0.75, markeredgecolor='none')
	PDFDots, = ax.plot(range(pdf[1][0]-1, pdf[-1][0]), estPDF, c='green', alpha=0.75, markeredgecolor='none')
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_ylabel('Proportion of Users')
	ax.set_xlabel('Number of Friends')
	plt.show()

# def userRevHist():
# 	revs = dbHelper.selectUsers("review_count")
# 	print revs[0]
# 	revCounts = []
# 	for rev in revs:
# 		revCounts.append(int(rev["review_count"]))

# 	n, bins, patches = plt.hist(revCounts, 100, range = (0, 200), normed=1, log = True, facecolor='blue', alpha=0.75)
# 	plt.xlabel('Number of Reviews')
# 	plt.xscale('log')
# 	plt.ylabel('Proportion of Users')
# 	plt.show()

def userRevHist():
	revs = dbHelper.selectUsers("review_count")
	revCounts = {}
	for rev in revs:
		count = int(rev["review_count"])
		if count in revCounts:
			revCounts[count] += 1
		else:
			revCounts[count] = 1
	x = []
	y = []
	numUsers = len(revs)
	for count in revCounts:
		x.append(count)
		y.append(revCounts[count])

	fig = plt.figure()
	ax = plt.gca()
	G1Dots, = ax.plot(x , [float(i) / float(numUsers) for i in y], 'o', c='blue', alpha=0.75, markeredgecolor='none')
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_ylabel('Proportion of Users')
	ax.set_xlabel('Number of Reviews')
	plt.show()


# def busRevHist():
# 	revs = dbHelper.selectBusinesses("review_count")
# 	revCounts = []
# 	for rev in revs:
# 		revCounts.append(int(rev["review_count"]))

# 	n, bins, patches = plt.hist(revCounts, 100, normed=1, log = True, facecolor='blue', alpha=0.75)
# 	plt.xlabel('Number of Reviews')
# 	plt.ylabel('Proportion of Businesses')
# 	plt.xscale('log')
# 	plt.show()

def busRevHist():
	revs = dbHelper.selectBusinesses("review_count")
	revCounts = {}
	for rev in revs:
		count = int(rev["review_count"])
		if count in revCounts:
			revCounts[count] += 1
		else:
			revCounts[count] = 1
	x = []
	y = []
	numUsers = len(revs)
	for count in revCounts:
		x.append(count)
		y.append(float(revCounts[count]) / float(numUsers))

	fig = plt.figure()
	ax = plt.gca()
	G1Dots, = ax.plot(x , y, 'o', c='blue', alpha=0.75, markeredgecolor='none')
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_ylabel('Proportion of Businesses')
	ax.set_xlabel('Number of Reviews')
	plt.show()


if __name__ == "__main__":
	# userNet = createFriendNetwork()
	# GraphClustCoeff = snap.GetClustCf(userNet, -1)
	# print "Clustering coefficient: %f" % GraphClustCoeff

	# randNet = snap.GenRndGnm(snap.PUNGraph, userNet.GetNodes(), userNet.GetEdges())
	# RGraphClustCoeff = snap.GetClustCf(randNet, -1)
	# print "Random clustering coefficient: %f" % RGraphClustCoeff
	# plotDegDistr(userNet)

	# userRevHist()
	busRevHist()
	
