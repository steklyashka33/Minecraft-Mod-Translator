BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Languages" (
	"row"	INTEGER,
	"Labels"	TEXT UNIQUE,
	"English"	TEXT NOT NULL,
	"Rusian"	TEXT NOT NULL,
	PRIMARY KEY("row" AUTOINCREMENT)
);
INSERT INTO "Languages" VALUES (1,'title_label','','');
INSERT INTO "Languages" VALUES (2,'create_button','Create','Создать');
INSERT INTO "Languages" VALUES (3,NULL,'','');
COMMIT;
