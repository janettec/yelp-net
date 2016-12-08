DROP TABLE IF EXISTS Businesses;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Friends;

--ROWID is implicit
CREATE TABLE Businesses (
	--ROWID INTEGER NOT NULL,
	business_id TEXT NOT NULL,
	name TEXT,
	stars REAL NOT NULL,
	city TEXT,
	state TEXT,
	longitude REAL,
	latitude REAL,
	review_count INTEGER,
	price_range INTEGER,
	PRIMARY KEY (business_id)
);

CREATE TABLE Users (
	--ROWID INTEGER NOT NULL,
	user_id TEXT NOT NULL,
	average_stars REAL,
	review_count INTEGER,
	fans INTEGER,
	yelping_since DATE,
	PRIMARY KEY (user_id)
);

CREATE TABLE Reviews (
	--ROWID INTEGER NOT NULL,
	review_id TEXT NOT NULL,
	user_id TEXT NOT NULL,
	business_id TEXT NOT NULL,
	stars INTEGER,
	review TEXT,
	date DATE,
	PRIMARY KEY (review_id),
	FOREIGN KEY (business_id) REFERENCES Businesses(business_id)
);

CREATE TABLE Categories (
	--ROWID INTEGER NOT NULL,
	business_id TEXT NOT NULL,
	category TEXT NOT NULL,
	PRIMARY KEY (business_id, category),
	FOREIGN KEY (business_id) REFERENCES Businesses(business_id)
);

CREATE TABLE Friends (
	--ROWID INTEGER NOT NULL,
	user1 TEXT NOT NULL,
	user2 TEXT NOT NULL,
	PRIMARY KEY (user1, user2),
	FOREIGN KEY (user1) REFERENCES Users(user_id)
);