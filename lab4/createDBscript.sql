CREATE TABLE IF NOT EXISTS "Tournaments" (
"id"	INTEGER,
"name"	TEXT,
"city"	TEXT,
"begin"	TEXT,
"system"	TEXT,
"tours_count"	INTEGER,
"min_rating"	INTEGER,
"time_on_game"	INTEGER,
PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "Prizes" (
	"id"	INTEGER,
	"tournament_id"	INTEGER,
	"place"	INTEGER,
	"prize"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("tournament_id") REFERENCES "tournaments"("id")
);

CREATE TABLE IF NOT EXISTS "Songs" (
	"id"	INTEGER,
	"artist"	TEXT,
	"song"	TEXT,
	"duration_ms"	INTEGER,
	"year"	INTEGER,
	"tempo"	REAL,
	"genre"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "Products" (
	"id"	INTEGER,
	"name"	TEXT,
	"price"	REAL CHECK("price" >= 0),
	"quantity"	INTEGER CHECK("quantity" >= 0),
	"category"	TEXT,
	"fromCity"	TEXT,
	"isAvailable"	INTEGER,
	"views"	INTEGER CHECK("views" >= 0),
	"changeCount"	INTEGER CHECK("changeCount" >= 0),
	PRIMARY KEY("id" AUTOINCREMENT)
);