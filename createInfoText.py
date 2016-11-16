from dbHelper import *
import re
import Stemmer
from nltk.corpus import stopwords

stops = set(stopwords.words('english'))
stemmer = Stemmer.Stemmer("english")
file = open("graphAttributes.txt", "w+")

users = selectUsers("rowid, *")
user_count = 0
for user in users:
	user_count += 1
	if user_count % 500 == 0:
		print "User %s" % user_count
	user_id = user["user_id"]
	reviews = selectFromWhere("Reviews.business_id, Reviews.stars, Reviews.review", "Users LEFT OUTER JOIN Reviews " + \
										"ON Users.user_id = Reviews.user_id", "Users.user_id = \"%s\"" % user_id)
	review_set = set()
	wordMap = {}
	for review in reviews:
		review_set.add((review["business_id"], review["stars"]))
		review_text = review["review"]
		review_arr = re.findall(r"[\w']+", review_text)
		for word in review_arr:
			word = stemmer.stemWord(word.lower())
			if word not in stops:
				if word not in wordMap:
					wordMap[word] = 0
				wordMap[word] += 1
	friends = selectFromWhere("Friends.user2", "Users LEFT OUTER JOIN Friends " +\
									 "ON Users.user_id = Friends.user1", "Users.user_id = \"%s\"" % user_id)
	friend_set = set()
	for friend in friends:
		friend_set.add(friend["user2"])
	line = user_id + "|"
	wroteReview, wroteFriend, wroteWords = False, False, False
	for business_id, stars in review_set:
		if business_id is not None and stars is not None:
			if wroteFriend:
				line += ","
			line += "%s,%s" % (business_id, stars)
			wroteFriend = True
	line += "|"
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
