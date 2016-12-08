from dbHelper import *
from snap import *

file = open("EdgeListLasVegas.txt", "w+")
users = selectUsers("rowid, *")
rowToUser = {}
num_user = 0
for user in users:
	num_user += 1
	if num_user % 10000 == 0:
		print "User ", num_user
	row_id = user["rowid"]
	user_id = user["user_id"]
	friends = selectFriendsOfUser(user_id)
	for friend in friends:
			friend_id = friend["user2"]
			if friend_id is not None:
				friend_row_id = selectUsers("rowid", 'user_id = "%s"' % friend_id)[0]["rowid"]
				file.write("%s, %s\n" % (row_id, friend_row_id))