"""
Generates news JSON files
Generally you're expected to update the game versions manually
as for most games you only ever want the latest version (supported) of the game
"""
from ast import Constant
import news_feed as feed
import constants
import json
import os
import argparse

from datetime import datetime, timedelta


OUTPUT_DIR = "news"

def create_merged_feed(*news_lists, limit=constants.DAYS_LIMIT):
    """
    Merge multiple news feeds into a singular one
    limit = maximum number of days old to be included in the merged feed
    """
    merged_feed = []
    for news_list in news_lists:
        merged_feed.extend(news_list)
    cutoff_date = datetime.now() - timedelta(days=limit)
    filtered_feed = [news for news in merged_feed if datetime.fromtimestamp(news['timestamp']) >= cutoff_date]
    sorted_feed = sorted(filtered_feed, key=lambda x: x['timestamp'], reverse=True)
    return sorted_feed

def attach_news_meta_data(news_data: list):
    """
    Attaches additional metadata to news data files
    Currently this is only the time of completion
    """
    return {
        "fetch_time": int(datetime.now().timestamp()),
        "news_posts": news_data
    }

def log_output(message: str, type: str="DEBUG"):
    """
    Prints a log line output with a timestamp
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{type}]: {message}")

def generate_news_file(filename, url, version=None):
    log_output(f"Fetching {filename.upper()} News Data", "NEWS")
    news_data = feed.get_news(url, version) if version else feed.get_news(url)
    if len(news_data) != 0:
        log_output(f"Success. Got {filename.upper()} News Data. Saving to file...", "NEWS")
        with open(f"{OUTPUT_DIR}/{filename}.json", 'w') as json_file:
            json.dump(attach_news_meta_data(news_data), json_file)
    elif os.path.exists(f"{OUTPUT_DIR}/{filename}.json"):
        print(f"Failed. Couldn't fetch {filename.upper()} data. Using previously scraped data", "NEWS")
        with open(f"{OUTPUT_DIR}/{filename}.json", 'r') as json_file:
            news_data = json.load(json_file)['news_posts']
    else:
        print(f"Failed. Couldn't fetch {filename.upper()} data. Skipping...", "NEWS")
    return news_data

# For e-amusement games you can choose to pull from a specific implementation of the scraper or the generic feed provided
# by the e-amusement app. Information is different
def generate_iidx_news_file(eamuse_feed: bool=False):
    if eamuse_feed:
        return generate_news_file("iidx_news", constants.EAMUSE_APP_FEED, constants.IIDX_EAMUSE_APP_ID)
    else:
        return generate_news_file("iidx_news", constants.IIDX_PINKY_CRUSH_NEWS_SITE)

def generate_sdvx_news_file():
    return generate_news_file("sdvx_news", constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)

def generate_ddr_news_file(eamuse_feed: bool=False):
    if eamuse_feed:
        return generate_news_file("ddr_news", constants.EAMUSE_APP_FEED, constants.DDR_EAMUSE_APP_ID)
    else:
        return generate_news_file("ddr_news", constants.DDR_WORLD_NEWS_SITE)

def generate_chunithm_jp_news_file():
    return generate_news_file("chunithm_jp_news", constants.CHUNITHM_JP_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)

def generate_maimaidx_jp_news_file():
    return generate_news_file("maimaidx_jp_news", constants.MAIMAIDX_JP_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM_PLUS)

def generate_ongeki_jp_news_file():
    return generate_news_file("ongeki_jp_news", constants.ONGEKI_JP_NEWS_SITE, constants.ONGEKI_VERSION.REFRESH)

def generate_maimaidx_intl_news_file():
    return generate_news_file("maimaidx_intl_news", constants.MAIMAIDX_INTL_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM)

def generate_chunithm_intl_news_file():
    return generate_news_file("chunithm_intl_news", constants.CHUNITHM_INTL_NEWS_SITE, constants.CHUNITHM_VERSION.LUMINOUS_PLUS)

if __name__ == "__main__":
    log_output("JOB START", "TASK")
    if not os.path.exists(OUTPUT_DIR):
        log_output(f"{OUTPUT_DIR} was not found. Creating this directory...")
        os.makedirs(OUTPUT_DIR)

    iidx_news_data = generate_iidx_news_file(eamuse_feed=True)
    sdvx_news_data = generate_sdvx_news_file()
    ddr_news_data = generate_ddr_news_file(eamuse_feed=True)
    chunithm_jp_news_data = generate_chunithm_jp_news_file()
    maimaidx_jp_news_data = generate_maimaidx_jp_news_file()
    ongeki_jp_news_data = generate_ongeki_jp_news_file()
    maimaidx_intl_news_data = generate_maimaidx_intl_news_file()
    chunithm_intl_news_data = generate_chunithm_intl_news_file()

    news = create_merged_feed(
        iidx_news_data,
        sdvx_news_data,
        ddr_news_data,
        chunithm_jp_news_data,
        maimaidx_jp_news_data,
        ongeki_jp_news_data,
        maimaidx_intl_news_data,
        chunithm_intl_news_data
    )
    log_output("Creating merged news.json file for all news that are within " + str(constants.DAYS_LIMIT) + " days old")
    with open(OUTPUT_DIR+'/news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(news), json_file)
    log_output("JOB DONE", "TASK")
