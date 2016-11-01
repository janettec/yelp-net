import sqlite3
import json

conn = sqlite3.connect('Yelp.db')
sqliteScript = conn.executescript(open("schema.sql", "r").read())

print "Opening businesses"
file = open("yelp_academic_dataset_business.json", "r")
print "Parsing businesses"
business_count = 0
for line in file:
	business_count += 1
	if business_count % 20000 == 0:
		print "#" + str(business_count)
	c = conn.cursor()
	parsed = json.loads(line)

	business_id = parsed["business_id"]
	review_count = int(parsed["review_count"])
	name = parsed["name"]
	longitude = float(parsed["longitude"])
	latitude = float(parsed["latitude"])
	state = parsed["state"]
	stars = float(parsed["stars"])
	attributeMap = parsed["attributes"]
	price_range = 0 if "Price Range" not in attributeMap else attributeMap["Price Range"]

	newTuple = (business_id, name, stars, state, longitude, latitude, review_count, price_range)
	c.execute("INSERT INTO Businesses VALUES (?, ?, ?, ?, ?, ?, ?, ?)", newTuple)

	categories = parsed["categories"]
	for category in categories:
		c.execute("INSERT INTO Categories VALUES (?, ?)", (business_id, category))
print "Committing businesses"
conn.commit()
print "Finished %s businesses \n" % business_count

print "Opening users"
file = open("yelp_academic_dataset_user.json", "r")
print "Parsing users"
user_count = 0
for line in file:
	user_count += 1
	if user_count % 200000 == 0:
		print "#" + str(user_count)
	c = conn.cursor()
	parsed = json.loads(line)

	user_id = parsed["user_id"]
	average_stars = float(parsed["average_stars"])
	review_count = int(parsed["review_count"])
	fans = int(parsed["fans"])
	yelping_since = parsed["yelping_since"] + "-01"
	c.execute("INSERT INTO Users VALUES (?, ?, ?, ?, ?)", (user_id, average_stars, review_count, fans, yelping_since))
print "Committing users"
conn.commit()
print "Finished %s users \n" % user_count
	
print "Opening reviews"
file = open("yelp_academic_dataset_review.json", "r")
print "Parsing reviews"
review_count = 0
for line in file:
	review_count += 1
	if review_count % 500000 == 0:
		print "#" + str(review_count)
	c = conn.cursor()
	parsed = json.loads(line)

	review_id = parsed["review_id"]
	user_id = parsed["user_id"]
	business_id = parsed["business_id"]
	stars = int(parsed["stars"])
	review = parsed["text"]
	date = parsed["date"]
	c.execute("INSERT INTO Reviews VALUES (?, ?, ?, ?, ?, ?)", (review_id, user_id, business_id, stars, review, date))
print "Committing reviews"
conn.commit()
conn.close()
print "Finished %s reviews" % review_count

