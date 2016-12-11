import sqlite3
from datetime import datetime

#####################################################################################
# Schema
#####################################################################################

# Businesses 
# 	business_id TEXT NOT NULL,
# 	name TEXT,
# 	stars REAL NOT NULL,
# 	state TEXT,
# 	longitude REAL,
# 	latitude REAL,
# 	review_count INTEGER,
# 	price_range INTEGER

# Users 
# 	user_id TEXT NOT NULL,
# 	average_stars REAL,
# 	review_count INTEGER,
# 	fans INTEGER,
# 	yelping_since DATE

# Reviews
# 	review_id TEXT NOT NULL,
# 	user_id TEXT NOT NULL,
# 	business_id TEXT NOT NULL,
# 	stars INTEGER,
# 	review TEXT,
# 	date DATE

# Categories
# 	business_id TEXT NOT NULL,
# 	category TEXT NOT NULL

##########################################################################################
# Implementation
##########################################################################################

conn = sqlite3.connect('YelpWaterloo.db')
conn.row_factory = sqlite3.Row

# Treats string as SQL query and executes it
# @returns: [SQLite Cursor]
def executeQuery(string):
	return conn.execute(string).fetchall()

# Generic select, from, where
# @returns: [SQLite Cursor]
def selectFromWhere(select, from_clause, where="1=1"):
	return executeQuery("SELECT %s FROM %s WHERE %s" % (select, from_clause, where))

def selectBusinesses(select, where="1=1"):
	return selectFromWhere(select, "(SELECT Businesses.*, category FROM Businesses " + \
		"LEFT OUTER JOIN Categories ON Businesses.business_id = Categories.business_id)", where + " ORDER BY business_id")

def selectUsers(select, where="1=1"):
	return selectFromWhere(select, "Users", where)

def selectFriendsOfUser(user_id, additional_where="1=1"):
	return selectFromWhere("user2", "Users LEFT OUTER JOIN Friends ON user_id = user1", "user_id = \"%s\" AND %s" % (user_id, additional_where))

def selectReviews(select, where="1=1"):
	return selectFromWhere(select, "Reviews", where)

# Reviews is a huge table, so it may be better to stream the results if the result set is huge
# Tested: If pulling the text of the reviews, stream. Otherwise, just do normally.
# Creates a closure that when ran, returns <quantity> number of results. 
# lastReviewID is expected to be None when called manually
# Usage:
#
# 	closure = selectReviewsStream(quantity, None, select, where)
# 	while closure is not None:
#			result, closure = closure()
#			...do something with results...
#
def selectReviewsStream(quantity, lastReviewID, select, where="1=1"):
	if quantity <= 0:
		raise ValueError("Quantity must be greater than 0! It doesn't make sense to pull 0 elements.")
	# Closure that you can keep calling to get pair (next <quantity> results, closure)
	def streamReviewClosure():		
		actualWhere = where
		if lastReviewID is not None:
			actualWhere += (" AND ROWID > " + str(lastReviewID))
		queryResults = selectFromWhere("ROWID, " + select, "Reviews", actualWhere + " ORDER BY ROWID LIMIT " + str(quantity))
		newLastReviewID = None
		newClosure = None
		if len(queryResults) > 0:
			newLastReviewID = queryResults[len(queryResults) - 1]["ROWID"]
			newClosure = selectReviewsStream(quantity, newLastReviewID, select, where)
		return queryResults, newClosure
	return streamReviewClosure

def stringToDate(string):
	return datetime.strptime(string, '%Y-%m-%d')

def unicodeToAscii(uni):
	return uni.encode('ascii', 'ignore')