from enum import Enum

DAYS_LIMIT=14

SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE ="https://p.eagate.573.jp/game/sdvx/vi/news/index.html"
IIDX_PINKY_CRUSH_NEWS_SITE="https://p.eagate.573.jp/game/2dx/32/info/index.html"
DDR_WORLD_NEWS_SITE="https://p.eagate.573.jp/game/ddr/ddrworld/info/index.html"

EAMUSE_APP_FEED="https://eam.573.jp/app/web/post/official"
IIDX_EAMUSE_APP_ID="s8svjrq62x592gvb"
SDVX_EAMUSE_APP_ID="3215emnco2s2p1sx"
DDR_EAMUSE_APP_ID="aegmtuzekqik0eyf"
GITADORA_EAMUSE_APP_ID="9orw5gze0d1tkyhm"
POPN_MUSIC_EAMUSE_APP_ID="17ua1w2bg3aggz00"
NOSTALGIA_EAMUSE_APP_ID="mql0c9jmkhzf02r3"
JUBEAT_EAMUSE_APP_ID="bz6w0u3gp546fpnq"

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
