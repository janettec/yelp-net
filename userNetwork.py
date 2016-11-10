from snap import *
from dbHelper import *

def createFriendNetwork():
	userNetwork = LoadEdgeList(PUNGraph, "friend_edge_list.txt", 0, 1)
	noFriendUsers = selectUsers("ROWID", "user_id NOT IN (SELECT user1 FROM Friends)")
	for record in noFriendUsers:
		userNetwork.AddNode(int(record["ROWID"]))
	return userNetwork