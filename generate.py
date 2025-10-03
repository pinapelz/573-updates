"""
Generates news JSON files
Generally you're expected to update the game versions manually
as for most games you only ever want the latest version (supported) of the game
"""
import news_feed as feed
import constants
import json
import hashlib
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from database import Database
from feed import build_rss_from_news_feed
from notifications import check_can_send_notifs, broadcast_to_topic
from sega import maimaidx_intl

load_dotenv()

OUTPUT_DIR = "news"
ARCHIVE_NEWS = True
GENERATE_RSS_FEEDS = True
SEND_NOTIFICATIONS = True


def compute_json_hash(data):
    return hashlib.sha256(
        json.dumps(data, sort_keys=True).encode("utf-8")
    ).hexdigest()


def save_news_to_db(news_feed: list):
    log_output("Writing news to local save database. This is purely for archival reasons")
    database = Database()
    for entry in news_feed:
        key = compute_json_hash(entry)
        database.add_news_entry(key, entry)
    database.close()


def create_merged_feed(*news_lists, limit=constants.DAYS_LIMIT):
    """
    Generator-based memory-efficient merging of multiple news feeds.
    Only includes news newer than `limit` days.
    """
    cutoff = datetime.now() - timedelta(days=limit)
    recent_items = (
        item
        for news_list in news_lists
        if news_list
        for item in news_list
        if datetime.fromtimestamp(item["timestamp"]) >= cutoff
    )
    return sorted(recent_items, key=lambda x: x["timestamp"], reverse=True)


def attach_news_meta_data(news_data: list):
    """
    Attaches additional metadata to news data files
    Currently this is only the time of completion
    """
    return {
        "fetch_time": int(datetime.now().timestamp()),
        "news_posts": news_data,
    }

def attempt_broadcast_notifications(news_data: list, title: str, topic: str, image: str="http://arcade.moekyun.me/liris.webp", limit=constants.DAYS_LIMIT):
    if news_data and SEND_NOTIFICATIONS:
        if not check_can_send_notifs:
            print("[WARNING] Skipping notifications as env vars are not properly configured. See template")
        else:
            database = Database()
            cutoff = datetime.now() - timedelta(days=limit)
            for entry in news_data:
                if datetime.fromtimestamp(entry["timestamp"]) < cutoff:
                    continue
                news_id = compute_json_hash(entry)
                if database.check_news_id_exists(news_id):
                    continue
                else:
                    print("[Notifications] Broadcasting Unique News with id: " + news_id)
                    if entry.get("en_headline"):
                        body_text = entry["en_headline"]
                    elif entry.get("en_content"):
                        body_text = entry["en_content"]
                    elif entry.get("headline"):
                        body_text = entry["headline"]
                    else:
                        body_text = entry.get("content", "")
                    if len(body_text) > 50:
                        body_text = body_text[:50] + "..."
                    if entry.get("images"):
                        if len(entry.get("images")) >= 1:
                            image = entry.get("images")[0]["image"]
                    broadcast_to_topic(topic, title, body_text, image)



def log_output(message: str, type: str = "DEBUG"):
    """
    Prints a log line output with a timestamp
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{type}]: {message}")


def generate_news_file(filename, url, version=None, formatted_name: str = None):
    log_output(f"Fetching {filename.upper()} News Data", "NEWS")
    news_data = None
    try:
        news_data = feed.get_news(url, version) if version else feed.get_news(url)
    except Exception as e:
        print(e)
        print("[ERROR] Wasn't able to fetch news. Skipping...")

    path = f"{OUTPUT_DIR}/{filename}.json"

    if news_data:
        log_output(f"Success. Got {filename.upper()} News Data. Saving to file...", "NEWS")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(attach_news_meta_data(news_data), f, indent=2, ensure_ascii=False)

    elif os.path.exists(path):
        log_output(
            f"Failed. Couldn't fetch {filename.upper()} data. Using previously scraped data",
            "NEWS",
        )
        with open(path, "r", encoding="utf-8") as json_file:
            news_data = json.load(json_file)["news_posts"]

    else:
        log_output(f"Failed. Couldn't fetch {filename.upper()} data. Skipping...", "NEWS")
        return news_data

    if GENERATE_RSS_FEEDS:
        rss_file_path = f"{OUTPUT_DIR}/{filename}.xml"
        log_output(f"Generating RSS Feed: {rss_file_path}")
        if not formatted_name:
            formatted_name = filename
        title = f"{formatted_name} News RSS Feed"
        description = f"The latest information for {formatted_name} from official sources"
        build_rss_from_news_feed(title, description, path, rss_file_path)

    return news_data


# For e-amusement games you can choose to pull from a specific implementation of the scraper or the generic feed provided
# by the e-amusement app. Information is different
def generate_iidx_news_file(eamuse_feed: bool=False):
    if eamuse_feed:
        return generate_news_file("iidx_news", constants.EAMUSE_APP_FEED, constants.IIDX_EAMUSE_APP_ID)
    else: # legacy should not be used,  use eamuse app feed above
        return generate_news_file("iidx_news", constants.IIDX_PINKY_CRUSH_NEWS_SITE)

def generate_sdvx_news_file():
    news = generate_news_file("sdvx_news", constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)
    attempt_broadcast_notifications(news, "New Information for SOUND VOLTEX","sdvx")
    return news

def generate_ddr_news_file(eamuse_feed: bool=False):
    if eamuse_feed:
        return generate_news_file("ddr_news", constants.EAMUSE_APP_FEED, constants.DDR_EAMUSE_APP_ID)
    else:
        return generate_news_file("ddr_news", constants.DDR_WORLD_NEWS_SITE)

def generate_polaris_chord_news_file():
    return generate_news_file("polaris_chord_news", constants.POLARIS_CHORD_NEWS_SITE)

def generate_dance_around_news_file():
    return generate_news_file("dance_around_news", constants.EAMUSE_APP_FEED, constants.DANCE_AROUND_APP_ID)

def generate_dance_rush_news_file():
    return generate_news_file("dance_rush_news", constants.EAMUSE_APP_FEED, constants.DANCE_RUSH_APP_ID)

def generate_popn_music_news_file():
    return generate_news_file("popn_music_news", constants.EAMUSE_APP_FEED, constants.POPN_MUSIC_EAMUSE_APP_ID)

def generate_jubeat_news_file():
    return generate_news_file("jubeat_news", constants.EAMUSE_APP_FEED, constants.JUBEAT_EAMUSE_APP_ID)

def generate_nostalgia_news_file():
    return generate_news_file("nostalgia_news", constants.EAMUSE_APP_FEED, constants.NOSTALGIA_EAMUSE_APP_ID)

def generate_gitadora_news_file():
    return generate_news_file("gitadora_news", constants.EAMUSE_APP_FEED, constants.GITADORA_EAMUSE_APP_ID)

def generate_chunithm_jp_news_file():
    return generate_news_file("chunithm_jp_news", constants.CHUNITHM_JP_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)

def generate_maimaidx_jp_news_file():
    news = generate_news_file("maimaidx_jp_news", constants.MAIMAIDX_JP_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM_PLUS)
    attempt_broadcast_notifications(news, "New information for maimai DX (Japan ver.)", "maimaidx_jp")
    return news

    return
def generate_ongeki_jp_news_file():
    return generate_news_file("ongeki_jp_news", constants.ONGEKI_JP_NEWS_SITE, constants.ONGEKI_VERSION.REFRESH)

def generate_maimaidx_intl_news_file():
    news = generate_news_file("maimaidx_intl_news", constants.MAIMAIDX_INTL_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM)
    attempt_broadcast_notifications(news, "New information for maimai DX (International ver.)", "maimaidx_intl")
    return news

def generate_chunithm_intl_news_file():
    return generate_news_file("chunithm_intl_news", constants.CHUNITHM_INTL_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)

def generate_idac_news_file():
    return generate_news_file("idac_news", constants.IDAC_NEWS_SITE)

def generate_music_diver_news_file():
    return generate_news_file("music_diver_news", constants.MUSIC_DIVER_NEWS)

def generate_street_fighter_news_file():
    return generate_news_file("street_fighter_news", constants.STREET_FIGHTER_NEWS_SITE, constants.STREET_FIGHTER_VERSION.SIX)

def generate_taiko_news_file():
    return generate_news_file("taiko_news", constants.TAIKO_BLOG_SITE)

def generate_wmmt_news_file():
    return generate_news_file("wmmt_news", constants.WANGAN_MAXI_GENERIC)

def generate_wacca_plus_news_file():
    if not os.environ.get("OPENAI_API_KEY"):
        print("[WARNING] Skipping WACCA PLUS generation, not possible without summarization key")
        return {}
    return generate_news_file("wacca_plus_news", constants.WACCA_PLUS_MAGIC_STRING)

def generate_museca_plus_news_file():
    return generate_news_file("museca_plus_news", constants.MUSECA_PLUS_NEWS_SITE)

def generate_rbdx_plus_news_file():
    return generate_news_file("rb_deluxe_plus_news", constants.RB_DELUXE_PLUS_NEWS)

if __name__ == "__main__":
    log_output("JOB START", "TASK")
    if not os.path.exists(OUTPUT_DIR):
        log_output(f"{OUTPUT_DIR} was not found. Creating this directory...")
        os.makedirs(OUTPUT_DIR)
    sdvx_news_data = generate_sdvx_news_file()
    polaris_news_data = generate_polaris_chord_news_file()
    iidx_news_data = generate_iidx_news_file(eamuse_feed=True)
    ddr_news_data = generate_ddr_news_file(eamuse_feed=True)
    dance_rush_news_data = generate_dance_rush_news_file()
    dance_around_news_data = generate_dance_around_news_file()
    gitadora_news_data = generate_gitadora_news_file()
    popn_music_news_data = generate_popn_music_news_file()
    jubeat_news_data = generate_jubeat_news_file()
    nostalgia_news_data = generate_nostalgia_news_file()
    chunithm_jp_news_data = generate_chunithm_jp_news_file()
    maimaidx_jp_news_data = generate_maimaidx_jp_news_file()
    ongeki_jp_news_data = generate_ongeki_jp_news_file()
    idac_news_data = generate_idac_news_file()
    maimaidx_intl_news_data = generate_maimaidx_intl_news_file()
    chunithm_intl_news_data = generate_chunithm_intl_news_file()
    music_diver_news_data = generate_music_diver_news_file()
    street_fighter_news_data = generate_street_fighter_news_file()
    taiko_news_data = generate_taiko_news_file()
    wacca_plus_news = generate_wacca_plus_news_file()
    museca_plus_news = generate_museca_plus_news_file()
    generate_rbdx_plus_news_file()
    wmmt_news = generate_wmmt_news_file()



    news = create_merged_feed(
        iidx_news_data,
        sdvx_news_data,
        ddr_news_data,
        gitadora_news_data,
        popn_music_news_data,
        jubeat_news_data,
        nostalgia_news_data,
        chunithm_jp_news_data,
        maimaidx_jp_news_data,
        ongeki_jp_news_data,
        idac_news_data,
        maimaidx_intl_news_data,
        chunithm_intl_news_data,
        music_diver_news_data,
        street_fighter_news_data,
        taiko_news_data,
        wacca_plus_news,
        museca_plus_news,
        polaris_news_data,
        dance_rush_news_data,
        dance_around_news_data,
        wmmt_news
    )
    log_output("Creating merged news.json file for all news that are within " + str(constants.DAYS_LIMIT) + " days old")
    if ARCHIVE_NEWS:
        save_news_to_db(news)
    with open(OUTPUT_DIR+'/news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(news), json_file)
    log_output("JOB DONE", "TASK")
