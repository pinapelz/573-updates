CREATE TABLE IF NOT EXISTS news (
    news_id VARCHAR(255) NOT NULL PRIMARY KEY,
    date TEXT NOT NULL,
    identifier TEXT NOT NULL,
    type TEXT,
    timestamp INTEGER NOT NULL,
    headline TEXT,
    content TEXT NOT NULL,
    url TEXT,
    is_ai_summary INTEGER NOT NULL DEFAULT 0,
    en_headline TEXT,
    en_content TEXT
);

CREATE TABLE IF NOT EXISTS news_images (
    news_id VARCHAR(255) NOT NULL PRIMARY KEY,
    image_url TEXT NOT NULL,
    link_url TEXT,
    FOREIGN KEY (news_id) REFERENCES news(news_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS summarization (
    id VARCHAR(255) PRIMARY KEY,
    headline TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS translation (
    id VARCHAR(255) PRIMARY KEY,
    source TEXT NOT NULL,
    result TEXT NOT NULL,
    source_lang TEXT NOT NULL,
    target_lang TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS wacplus (
    id VARCHAR(255) PRIMARY KEY,
    isNews INTEGER NOT NULL,
    type TEXT NOT NULL
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_news_date ON news(date);
CREATE INDEX IF NOT EXISTS idx_news_identifier ON news(identifier);
CREATE INDEX IF NOT EXISTS idx_news_timestamp ON news(timestamp);
CREATE INDEX IF NOT EXISTS idx_news_type ON news(type);
CREATE INDEX IF NOT EXISTS idx_news_is_ai_summary ON news(is_ai_summary);
CREATE INDEX IF NOT EXISTS idx_news_images_news_id ON news_images(news_id);
