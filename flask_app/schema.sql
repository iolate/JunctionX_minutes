
CREATE TABLE IF NOT EXISTS `minutes` (
    `idx` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` TEXT,
    `status` TEXT,
    `filename` TEXT,
    `filesize` INTEGER,
    `created_at` INTEGER,
    `is_private` INTEGER,
    `scripts` TEXT
);

CREATE TABLE IF NOT EXISTS `minutes_tags` (
	`idx` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`minutes_idx` NOT NULL INTEGER,
	`tag` TEXT
);