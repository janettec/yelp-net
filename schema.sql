DROP TABLE IF EXISTS Businesses;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Categories;

CREATE TABLE Businesses (
	business_id TEXT NOT NULL,
	name TEXT,
	stars REAL NOT NULL,
	state TEXT,
	longitude REAL,
	latitude REAL,
	review_count INTEGER,
	price_range INTEGER,
	PRIMARY KEY (business_id)
);

CREATE TABLE Users (
	user_id TEXT NOT NULL,
	average_stars REAL,
	review_count INTEGER,
	fans INTEGER,
	yelping_since DATE,
	PRIMARY KEY (user_id)
);

CREATE TABLE Reviews (
	review_id TEXT NOT NULL,
	user_id TEXT NOT NULL,
	business_id TEXT NOT NULL,
	stars INTEGER,
	review TEXT,
	date DATE,
	PRIMARY KEY (review_id)
	FOREIGN KEY (user_id) REFERENCES Users(user_id),
	FOREIGN KEY (business_id) REFERENCES Businesses(business_id)
);

CREATE TABLE Categories (
	business_id TEXT NOT NULL,
	category TEXT NOT NULL,
	PRIMARY KEY (business_id, category),
	FOREIGN KEY (business_id) REFERENCES Businesses(business_id)
);