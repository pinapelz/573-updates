from enum import Enum

DAYS_LIMIT=14

EAMUSEMENT_BASE_URL = "https://p.eagate.573.jp"
SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE ="https://p.eagate.573.jp/game/sdvx/vi/news/index.html"
IIDX_PINKY_CRUSH_NEWS_SITE="https://p.eagate.573.jp/game/2dx/32/info/index.html"

CHUNITHM_JP_NEWS_SITE="https://info-chunithm.sega.jp/"
MAIMAIDX_JP_NEWS_SITE="https://info-maimai.sega.jp/"
ONGEKI_JP_NEWS_SITE="https://info-ongeki.sega.jp/"

class CHUNITHM_VERSION(Enum):
    VERSE = 1

class MAIMAIDX_VERSION(Enum):
    PRISM = 1
    PRISM_PLUS = 2

class ONGEKI_VERSION(Enum):
    REFRESH = 1
