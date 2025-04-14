"""
Generates news JSON files
"""
import news_feed as feed
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

    print("Fetching SDVX Data")
    sdvx_news_data = feed.get_news(constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)
    if len(sdvx_news_data) != 0:
        with open(OUTPUT_DIR+'/sdvx_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(sdvx_news_data), json_file)

    print("Fetching CHUNITHM JPN Data")
    chunithm_jp_news_data = feed.get_news(constants.CHUNITHM_JP_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)
    if len(chunithm_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/chunithm_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(chunithm_jp_news_data), json_file)

    print("Fetching MAIMAI DX JPN Data")
    maimaidx_jp_news_data = feed.get_news(constants.MAIMAIDX_JP_NEWS_SITE, constants.MAIMAIDX_VERSION.PRISM_PLUS)
    if len(maimaidx_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/maimaidx_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(maimaidx_jp_news_data), json_file)

    print("Fetching ONGEKI JPN Data")
    ongeki_jp_news_data = feed.get_news(constants.ONGEKI_JP_NEWS_SITE, constants.ONGEKI_VERSION.REFRESH)
    if len(ongeki_jp_news_data) != 0:
        with open(OUTPUT_DIR+'/ongeki_jp_news.json', 'w') as json_file:
            json.dump(attach_news_meta_data(ongeki_jp_news_data), json_file)

    news = create_merged_feed(iidx_news_data, sdvx_news_data, chunithm_jp_news_data, maimaidx_jp_news_data, ongeki_jp_news_data)
    with open(OUTPUT_DIR+'/news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(news), json_file)
