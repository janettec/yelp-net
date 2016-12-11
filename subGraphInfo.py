''' 
Script assumes that graphs are saved as 'graphname.csv' where nodes are separated by commas
'''

import snap
import dbHelper

def createFriendNetwork(filename):
	userNetwork = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1, ',')
	noFriendUsers = dbHelper.selectUsers("ROWID", "user_id NOT IN (SELECT user1 FROM Friends)")
	for record in noFriendUsers:
		userNetwork.AddNode(int(record["ROWID"]))
	return userNetwork

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

	fig = plt.figure()
	ax = plt.gca()
	G1Dots, = ax.plot(deg , [float(x) / float(numNodes) for x in nodes], 'o', c='blue', alpha=0.75, markeredgecolor='none')
	ax.set_yscale('log')
	ax.set_xscale('log')
	ax.set_ylabel('Proportion of Users')
	ax.set_xlabel('Number of Friends')
	plt.show()

if __name__ == "__main__":
	G = createFriendNetwork("EdgeListLasVegas.csv")
	diam = snap.GetBfsFullDiam(G, 50000, False)
	print diam
	
