from abc import ABC, abstractmethod

class BaseDatabase(ABC):

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def add_new_wac_entry(self, key: str, is_news: bool, post_type: str):
        pass

    @abstractmethod
    def add_new_translation(self, key: str, source_lang: str,
                            target_lang: str, source_txt: str, result_txt: str):
        pass

    @abstractmethod
    def add_new_summary(self, key: str, headline: str, content: str):
        pass

    @abstractmethod
    def add_news_entry(self, key: str, news_entry: dict):
        pass

    @abstractmethod
    def get_summary(self, key: str):
        pass

    @abstractmethod
    def get_translation(self, key: str):
        pass

    @abstractmethod
    def get_wac_entry(self, key: str):
        pass

    @abstractmethod
    def check_news_id_exists(self, key: str) -> bool:
        pass
