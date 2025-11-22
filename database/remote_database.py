from database.base_database import BaseDatabase
import libsql


class RemoteDatabase(BaseDatabase):
    def __init__(self, url: str = None, auth_token: str = None, local_replica: str = None):
        """
        Initialize connection to Remote database using libsql (designed for Turso)
        """
        self._url = url
        self._auth_token = auth_token
        self._local_replica = local_replica or "new_db.db"

        if not self._url:
            raise ValueError("Database URL must be provided either as parameter or TURSO_DATABASE_URL environment variable")

        if not self._auth_token:
            raise ValueError("Auth token must be provided either as parameter or TURSO_AUTH_TOKEN environment variable")

        self._conn = libsql.connect(
            self._local_replica,
            sync_url=self._url,
            auth_token=self._auth_token
        )

        # Initial sync to get latest data
        self._conn.sync()
        self._initialize_db()

    def _initialize_db(self):
        """Initialize database schema"""
        with open("schema.sql") as f:
            # Execute schema creation
            self._conn.executescript(f.read())
            self._conn.commit()

    def close(self):
        """Close the database connection"""
        if self._conn:
            self._conn.close()

    def add_new_wac_entry(self, key: str, is_news: bool, post_type: str):
        """Add a new WAC entry to the database"""
        news_var = 0 if is_news is False else 1
        self._conn.execute(
            "INSERT OR REPLACE INTO wacplus (id, isNews, type) VALUES (?, ?, ?)",
            (key, news_var, post_type),
        )
        self._conn.commit()

    def add_new_translation(
        self,
        key: str,
        source_lang: str,
        target_lang: str,
        source_txt: str,
        result_txt: str,
    ):
        """Add a new translation to the database"""
        self._conn.execute(
            "INSERT OR REPLACE INTO translation (id, source_lang, target_lang, source, result) VALUES (?, ?, ?, ?, ?)",
            (key, source_lang, target_lang, source_txt, result_txt),
        )
        self._conn.commit()

    def add_new_summary(self, key: str, headline: str, content: str):
        """Add a new summary to the database"""
        self._conn.execute(
            "INSERT OR REPLACE INTO summarization (id, headline, content) VALUES (?, ?, ?)",
            (key, headline, content),
        )
        self._conn.commit()

    def add_news_entry(self, key: str, news_entry: dict):
        """Add a new news entry to the database"""
        is_ai_summary = 1 if news_entry.get("is_ai_summary", False) else 0
        en_headline = news_entry.get("en_headline", None)
        en_content = news_entry.get("en_content", None)
        headline = news_entry.get("headline", None)
        url = news_entry.get("url", None)

        self._conn.execute(
            "INSERT OR REPLACE INTO news (news_id, date, identifier, type, timestamp, headline, content, url, is_ai_summary, en_headline, en_content) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                key,
                news_entry["date"],
                news_entry["identifier"],
                news_entry["type"],
                news_entry["timestamp"],
                headline,
                news_entry["content"],
                url,
                is_ai_summary,
                en_headline,
                en_content,
            ),
        )

        # Add associated images
        for image_entry in news_entry["images"]:
            if image_entry["image"].startswith("data:"):
                continue
            link_url = image_entry.get("link", None)
            self._conn.execute(
                "INSERT OR REPLACE INTO news_images (news_id, image_url, link_url) VALUES (?, ?, ?)",
                (key, image_entry["image"], link_url),
            )
        self._conn.commit()

    def get_summary(self, key: str):
        """Get a summary by key"""
        result = self._conn.execute(
            "SELECT headline, content FROM summarization WHERE id = ?", (key,)
        ).fetchone()
        if result is None:
            return None
        return {"headline": result[0], "content": result[1]}

    def get_translation(self, key: str):
        """Get a translation by key"""
        result = self._conn.execute("SELECT result FROM translation WHERE id = ?", (key,)).fetchone()
        if result is None:
            return None
        return result[0]

    def get_wac_entry(self, key: str):
        """Get a WAC entry by key"""
        result = self._conn.execute("SELECT isNews, type FROM wacplus WHERE id = ?", (key,)).fetchone()
        if result is None:
            return None
        is_news = True if result[0] == 1 else False
        return is_news, result[1]

    def check_news_id_exists(self, key: str) -> bool:
        """
        Check if a news entry with the given ID exists in the database.

        :param key: The ID of the news entry to check.
        :return: True if the news entry exists, False otherwise.
        """
        result = self._conn.execute("SELECT 1 FROM news WHERE news_id = ?", (key,)).fetchone()
        return result is not None

    def sync(self):
        """Sync local changes with the remote database (Turso specific)"""
        self._conn.sync()

    def get_stats(self):
        """Get database statistics (useful for monitoring)"""
        stats = {}

        # Count records in each table
        tables = ['news', 'news_images', 'summarization', 'translation', 'wacplus']
        for table in tables:
            result = self._conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()
            count = result[0] if result else 0
            stats[f"{table}_count"] = count

        return stats
