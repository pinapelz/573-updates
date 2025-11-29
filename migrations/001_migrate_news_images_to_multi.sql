-- migrates old news image table from single images to multi per news
PRAGMA foreign_keys = OFF;
CREATE TABLE news_images_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_id VARCHAR(255) NOT NULL,
    image_url TEXT NOT NULL,
    link_url TEXT,
    FOREIGN KEY (news_id) REFERENCES news(news_id) ON DELETE CASCADE
);
INSERT INTO news_images_new (news_id, image_url, link_url)
SELECT news_id, image_url, link_url FROM news_images;
DROP TABLE news_images;
ALTER TABLE news_images_new RENAME TO news_images;
PRAGMA foreign_keys = ON;
