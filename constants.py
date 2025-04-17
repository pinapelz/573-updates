from enum import Enum

DAYS_LIMIT=14

EAMUSEMENT_BASE_URL = "https://p.eagate.573.jp"
SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE ="https://p.eagate.573.jp/game/sdvx/vi/news/index.html"
IIDX_PINKY_CRUSH_NEWS_SITE="https://p.eagate.573.jp/game/2dx/32/info/index.html"

CHUNITHM_JP_NEWS_SITE="https://info-chunithm.sega.jp/"
CHUNITHM_INTL_NEWS_SITE="https://info-chunithm.sega.com/"
MAIMAIDX_JP_NEWS_SITE="https://info-maimai.sega.jp/"
MAIMAIDX_INTL_NEWS_SITE="https://maimai.sega.com/download/"
ONGEKI_JP_NEWS_SITE="https://info-ongeki.sega.jp/"

ADD_EN_TRANSLATION=True # Only takes effect if an API key is provided in .env

class CHUNITHM_VERSION(Enum):
    LUMINOUS_PLUS = 1
    VERSE = 2

class MAIMAIDX_VERSION(Enum):
    PRISM = 1
    PRISM_PLUS = 2

class ONGEKI_VERSION(Enum):
    REFRESH = 1
