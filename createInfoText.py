from dbHelper import *
import re
import Stemmer
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
stemmer = Stemmer.Stemmer("english")
file = open("graphAttributes.txt", "w+")

print "Creating friends map."
friendsMap = {}
friends = selectFromWhere("user1, user2", "Friends")
for friend in friends:
	user1, user2 = friend["user1"], friend["user2"]
	if user1 not in friendsMap:
		friendsMap[user1] = set()
	friendsMap[user1].add(user2)
print "Finished creating friends map"

print "Creating review map."
reviewsMap = {}
reviews = selectFromWhere("review_id, user_id, business_id, stars", "Reviews")
for res in reviews:
	r_review_id = res["review_id"]
	r_user_id = res["user_id"]
	r_bus_id = res["business_id"]
	r_stars = res["stars"]
	if r_user_id not in reviewsMap:
		reviewsMap[r_user_id] = []
	reviewsMap[r_user_id].append((r_review_id, r_bus_id, r_stars))
print "Finished creating review map"

users = selectUsers("*")
user_count = 0
for user in users:

	user_count += 1
	if user_count % 500 == 0:
		print "User %s" % user_count
	user_id = user["user_id"]
	wroteReview, wroteFriend, wroteWords = False, False, False
	line = user_id + "|"

	reviews = []
	if user_id in reviewsMap:
		reviews = reviewsMap[user_id]
	review_set = set()
	wordMap = {}
	for review in reviews:
		review_id, business_id, stars = review
		if wroteReview:
			line += ","
		line += ("%s,%s" % (business_id, stars))
		wroteReview = True
		review_text = selectFromWhere("review", "Reviews", "review_id=\"%s\"" % review_id)[0]["review"]
		review_arr = re.findall(r"[\w']+", review_text)
		for word in review_arr:
			word = stemmer.stemWord(word.lower())
			if word not in stops:
				if word not in wordMap:
					wordMap[word] = 0
				wordMap[word] += 1
	line += "|"

	friend_set = None
	if user_id in friendsMap:
		friend_set = friendsMap[user_id]
	else:
		friend_set = []

	for friend in friend_set:
		if friend is not None:
			if wroteFriend:
				line += ","
			line += friend
			wroteFriend = True
	line += "|"

	for word, count in wordMap.items():
		if wroteWords:
			line += ","
		line += "%s,%s" % (word, count)
		wroteWords = True

	file.write(line + "\n")
file.close()
