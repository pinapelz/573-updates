"""
Generates news JSON files
"""
import news_feed as feed
import requests
import constants
import json
import os

from datetime import datetime, timedelta


OUTPUT_DIR = "news"

def create_merged_feed(*news_lists):
    merged_feed = []
    for news_list in news_lists:
        merged_feed.extend(news_list)
    cutoff_date = datetime.now() - timedelta(days=constants.DAYS_LIMIT)
    filtered_feed = [news for news in merged_feed if datetime.fromtimestamp(news['timestamp']) >= cutoff_date]
    sorted_feed = sorted(filtered_feed, key=lambda x: x['timestamp'], reverse=True)
    return sorted_feed

def fetch_json_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def attach_news_meta_data(news_data: list):
    return {
        "fetch_time": int(datetime.now().timestamp()),
        "news_posts": news_data
    }

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print("Fetching IIDX Data")
    iidx_news_data = feed.get_news(constants.IIDX_PINKY_CRUSH_NEWS_SITE)
    if len(iidx_news_data) != 0:
        with open(OUTPUT_DIR+'/iidx_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(iidx_news_data), json_file)
        print("IIDX Data fetched and saved.")
    elif len(iidx_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/iidx_news.json'):
        with open(OUTPUT_DIR+'/iidx_news.json', 'r') as json_file:
            iidx_news_data = json.load(json_file)['news_posts']
        print("IIDX Data not fetched, using existing data.")

    print("Fetching SDVX Data")
    sdvx_news_data = feed.get_news(constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)
    if len(sdvx_news_data) != 0:
        with open(OUTPUT_DIR+'/sdvx_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(sdvx_news_data), json_file)
        print("SDVX Data fetched and saved.")
    elif len(sdvx_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/sdvx_news.json'):
        with open(OUTPUT_DIR+'/sdvx_news.json', 'r') as json_file:
            sdvx_news_data = json.load(json_file)['news_posts']
        print("SDVX Data not fetched, using existing data.")

    print("Fetching CHUNITHM JPN Data")
    chunithm_jp_news_data = feed.get_news(constants.CHUNITHM_JP_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)
    if len(chunithm_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/chunithm_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(chunithm_jp_news_data), json_file)
        print("CHUNITHM JPN Data fetched and saved.")
    elif len(chunithm_jp_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/chunithm_jp_news.json'):
        with open(OUTPUT_DIR+'/chunithm_jp_news.json', 'r') as json_file:
            chunithm_jp_news_data = json.load(json_file)['news_posts']
        print("CHUNITHM JPN Data not fetched, using existing data.")

    print("Fetching MAIMAI DX JPN Data")
    maimaidx_jp_news_data = feed.get_news(constants.MAIMAIDX_JP_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM_PLUS)
    if len(maimaidx_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/maimaidx_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(maimaidx_jp_news_data), json_file)
        print("MAIMAI DX JPN Data fetched and saved.")
    elif len(maimaidx_jp_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/maimaidx_jp_news.json'):
        with open(OUTPUT_DIR+'/maimaidx_jp_news.json', 'r') as json_file:
            maimaidx_jp_news_data = json.load(json_file)['news_posts']
        print("MAIMAI DX JPN Data not fetched, using existing data.")

    print("Fetching ONGEKI JPN Data")
    ongeki_jp_news_data = feed.get_news(constants.ONGEKI_JP_NEWS_SITE, constants.ONGEKI_VERSION.REFRESH)
    if len(ongeki_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/ongeki_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(ongeki_jp_news_data), json_file)
        print("ONGEKI JPN Data fetched and saved.")
    elif len(ongeki_jp_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/ongeki_jp_news.json'):
        with open(OUTPUT_DIR+'/ongeki_jp_news.json', 'r') as json_file:
            ongeki_jp_news_data = json.load(json_file)['news_posts']
        print("ONGEKI JPN Data not fetched, using existing data.")

    print("Fetching MAIMAIDX INTL Data")
    maimaidx_intl_news_data = feed.get_news(constants.MAIMAIDX_INTL_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM)
    if len(maimaidx_intl_news_data) != 0:
        with open(OUTPUT_DIR+'/maimaidx_intl_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(maimaidx_intl_news_data), json_file)
        print("MAIMAIDX INTLN Data fetched and saved.")
    elif len(maimaidx_intl_news_data) == 0 and os.path.exists(OUTPUT_DIR+'/maimaidx_intl_news.json'):
        with open(OUTPUT_DIR+'/maimaidx_intl_news.json', 'r') as json_file:
            maimaidx_intl_news_data = json.load(json_file)['news_posts']
        print("MAIMAIDX INTL Data not fetched, using existing data.")

    news = create_merged_feed(iidx_news_data, sdvx_news_data, chunithm_jp_news_data, maimaidx_jp_news_data, ongeki_jp_news_data, maimaidx_intl_news_data)
    with open(OUTPUT_DIR+'/news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(news), json_file)
