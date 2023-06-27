BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "questions" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"question"	TEXT,
	"correct"	TEXT,
	"wrong"	TEXT
);
CREATE TABLE IF NOT EXISTS "members" (
	"MemberID"	INTEGER NOT NULL UNIQUE,
	"MemberName"	TEXT,
	PRIMARY KEY("MemberID")
);
INSERT INTO "questions" VALUES (1,'Test Quest','Correct Answer','Wrong Answer');
INSERT INTO "questions" VALUES (2,'Test Quest','Correct Answer','Wrong Answer;Wrong Answer');
INSERT INTO "questions" VALUES (3,'Test Quest','Correct Answer','Wrong Answer;Wrong Answer;Wrong Answer');
INSERT INTO "questions" VALUES (4,'Test Quest','Correct Answer;Correct Answer','Wrong Answer;Wrong Answer;Wrong Answer;Wrong Answer');
INSERT INTO "questions" VALUES (5,'Test Quest','Correct Answer;Correct Answer;Correct Answer','Wrong Answer;Wrong Answer;Wrong Answer;Wrong Answer;Wrong Answer');
COMMIT;
