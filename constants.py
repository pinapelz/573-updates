from enum import Enum

DAYS_LIMIT=14

SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE ="https://p.eagate.573.jp/game/sdvx/vi/news/index.html"
IIDX_PINKY_CRUSH_NEWS_SITE="https://p.eagate.573.jp/game/2dx/32/info/index.html"  # legacy should not be used,  eamuse feed is more verbose
DDR_WORLD_NEWS_SITE="https://p.eagate.573.jp/game/ddr/ddrworld/info/index.html"
POLARIS_CHORD_NEWS_SITE="https://p.eagate.573.jp/game/polarischord/pc/news/news.html"

EAMUSE_APP_FEED="https://eam.573.jp/app/web/post/official"
EAMUSE_APP_API_ROUTE="https://eam.573.jp/app/web/post/official"
EAMUSE_POST_SITE="https://eam.573.jp/app/web/post/detail.php"
IIDX_EAMUSE_APP_ID="s8svjrq62x592gvb"
SDVX_EAMUSE_APP_ID="3215emnco2s2p1sx"
DDR_EAMUSE_APP_ID="aegmtuzekqik0eyf"
GITADORA_EAMUSE_APP_ID="9orw5gze0d1tkyhm"
POPN_MUSIC_EAMUSE_APP_ID="17ua1w2bg3aggz00"
NOSTALGIA_EAMUSE_APP_ID="mql0c9jmkhzf02r3"
JUBEAT_EAMUSE_APP_ID="bz6w0u3gp546fpnq"
DANCE_AROUND_APP_ID="kmhqpindcodm0mkh"
DANCE_RUSH_APP_ID="ns3maqirvf08ddhp"

CHUNITHM_JP_NEWS_SITE="https://info-chunithm.sega.jp/"
CHUNITHM_INTL_NEWS_SITE="https://info-chunithm.sega.com/"
MAIMAIDX_JP_NEWS_SITE="https://info-maimai.sega.jp/"
MAIMAIDX_INTL_NEWS_SITE="https://maimai.sega.com/assets/data/index.json"
ONGEKI_JP_NEWS_SITE="https://info-ongeki.sega.jp/"
IDAC_NEWS_SITE="https://info-initialdac.sega.jp/"

MUSIC_DIVER_NEWS="https://mypage.musicdiver.jp/api/news?lang=en"
STREET_FIGHTER_NEWS_SITE="https://sf6ta.jp/info/list"

TAIKO_BLOG_SITE="https://taiko-ch.net/blog/"
WANGAN_MAXI_GENERIC="https://wanganmaxi-official.com/"
WANGAN_MAXI_NA_NEWS_SITE="https://wanganmaxi-official.com/wanganmaxi5dxplus/na/archive"
WANGAN_MAXI_ASIA_OCE_NEWS_SITE="https://wanganmaxi-official.com/wanganmaxi6rr/en/archive/"
WANGAN_MAXI_JP_NEWS_SITE="https://wanganmaxi-official.com/wanganmaxi6rrplus/jp/archive/"
WANGAN_MAXI_POSTS_PER_SECTION=3
# due to how dead the NA version is, these will be merged into a singular feed

ADD_EN_TRANSLATION=True # Only takes effect if an API key is provided in .env
CHUNI_RECURSIVE_IMAGE=True # Scrape the individual post pages and get all images there

WACCA_PLUS_MAGIC_STRING="1206017527864369262"
MUSECA_PLUS_NEWS_SITE="https://museca.plus/"
RB_DELUXE_PLUS_NEWS="https://dxplus.chilundui.com/"

RSS_FEED_URL="https://arcade-news.pinapelz.com"

class CHUNITHM_VERSION(Enum):
    LUMINOUS_PLUS = 1
    VERSE = 2
    X_VERSE = 3

class MAIMAIDX_VERSION(Enum):
    PRISM = 1
    PRISM_PLUS = 2
    CIRCLE = 3

class ONGEKI_VERSION(Enum):
    REFRESH = 1

class WANGAN_MAXI_VERSION(Enum):
    FIVE_DX_PLUS = 1,
    SIX = 2,
    SIX_R = 3,
    SIX_RR = 4,
    SIX_RR_PLUS = 5

class STREET_FIGHTER_VERSION(Enum):
    SIX = 1,
