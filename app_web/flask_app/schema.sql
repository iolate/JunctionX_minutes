
CREATE TABLE IF NOT EXISTS `minutes` (
    `idx` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `name` TEXT,
    `video_duration` INTEGER,
    `status` TEXT,
    `filename` TEXT,
    `filesize` INTEGER,
    `created_at` INTEGER,
    `is_private` INTEGER,
    `memo` TEXT,
    `scripts` TEXT
);

CREATE TABLE IF NOT EXISTS `minutes_tags` (
	`idx` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`minutes_idx` INTEGER NOT NULL,
	`tag` TEXT
);