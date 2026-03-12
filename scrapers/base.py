from abc import ABC, abstractmethod


class NewsSource(ABC):

    @abstractmethod
    def fetch(self, version=None) -> list[dict]:
        pass
