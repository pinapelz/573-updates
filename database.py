import json
import os
import sqlite3


class Database:
    def __init__(self):
        self._conn = sqlite3.connect("news.db")
        self._cursor = self._conn.cursor()
        self._initialize_db()
        self._migrate_old_data()

    def _initialize_db(self):
        with open("schema.sql") as f:
            self._cursor.executescript(f.read())
            self._conn.commit()

    def close(self):
        """Close the database connection"""
        if self._conn:
            self._conn.close()

    def _migrate_old_data(self):
        """
        Migrates old summarization, tl and wac files into DB
        """
        if os.path.exists("summarization_cache.json"):
            print("[Database] Migrating old summarization_cache to DB")
            with open("summarization_cache.json", "r") as file:
                summ_cache = json.load(file)
                for key, val in summ_cache.items():
                    self.add_new_summary(key, val["headline"], val["content"])
            os.rename("summarization_cache.json", "summarization_cache.json.bak")

        if os.path.exists("tl_cache.json"):
            print("[Database] Migrating old translation cache (tl_cache.json) to DB")
            with open("tl_cache.json", "r") as file:
                tl_cache = json.load(file)
                import hashlib

                for entry in tl_cache:
                    key = hashlib.sha256(
                        (
                            entry["source_lang"]
                            + entry["target_lang"]
                            + entry["source_txt"]
                        ).encode("utf-8")
                    ).hexdigest()
                    self.add_new_translation(
                        key,
                        entry["source_lang"],
                        entry["target_lang"],
                        entry["source_txt"],
                        entry["result_txt"],
                    )
                os.rename("tl_cache.json", "tl_cache.json.bak")

        if os.path.exists("wac_result_cache.json"):
            print("[Database] Migrating old WAC Data cache to DB")
            with open("wac_result_cache.json", "r") as file:
                wac_cache = json.load(file)
                import hashlib

                for key, value in wac_cache.items():
                    self.add_new_wac_entry(key, value[0], value[1])
                os.rename("wac_result_cache.json", "wac_result_cache.json.bak")

    def add_new_wac_entry(self, key: str, is_news: bool, post_type: str):
        news_var = 0 if is_news is False else 1
        self._cursor.execute(
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
        self._cursor.execute(
            "INSERT OR REPLACE INTO translation (id, source_lang, target_lang, source, result) VALUES (?, ?, ?, ?, ?)",
            (key, source_lang, target_lang, source_txt, result_txt),
        )
        self._conn.commit()

    def add_new_summary(self, key: str, headline: str, content: str):
        self._cursor.execute(
            "INSERT OR REPLACE INTO summarization (id, headline, content) VALUES (?, ?, ?)",
            (key, headline, content),
        )
        self._conn.commit()

    def add_news_entry(self, key: str, news_entry: dict):
        is_ai_summary = 1 if news_entry.get("is_ai_summary", False) else 0
        en_headline = news_entry.get("en_headline", None)
        en_content = news_entry.get("en_content", None)
        headline = news_entry.get("headline", None)
        url = news_entry.get("url", None)
        self._cursor.execute(
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
        for image_entry in news_entry["images"]:
            if image_entry["image"].startswith("data:"):
                continue
            link_url = image_entry.get("link", None)
            self._cursor.execute(
                "INSERT OR REPLACE INTO news_images (news_id, image_url, link_url) VALUES (?, ?, ?)",
                (key, image_entry["image"], link_url),
            )
        self._conn.commit()


    def get_summary(self, key: str):
        self._cursor.execute(
            "SELECT headline, content FROM summarization WHERE id = ?", (key,)
        )
        result = self._cursor.fetchone()
        if result is None:
            return None
        return {"headline": result[0], "content": result[1]}

    def get_translation(self, key: str):
        self._cursor.execute("SELECT result FROM translation WHERE id = ?", (key,))
        result = self._cursor.fetchone()
        if result is None:
            return None
        return result[0]

    def get_wac_entry(self, key: str):
        self._cursor.execute("SELECT isNews, type FROM wacplus WHERE id = ?", (key,))
        result = self._cursor.fetchone()
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
        self._cursor.execute("SELECT 1 FROM news WHERE news_id = ?", (key,))
        result = self._cursor.fetchone()
        return result is not None
