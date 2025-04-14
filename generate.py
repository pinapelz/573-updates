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

    iidx_news_data = feed.get_news(constants.IIDX_PINKY_CRUSH_NEWS_SITE)
    with open(OUTPUT_DIR+'/iidx_news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(iidx_news_data), json_file)

    sdvx_news_data = feed.get_news(constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)
    with open(OUTPUT_DIR+'/sdvx_news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(sdvx_news_data), json_file)

    chunithm_jp_news_data = feed.get_news(constants.CHUNITHM_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)
    with open(OUTPUT_DIR+'/chunithm_jp_news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(chunithm_jp_news_data), json_file)

    news = create_merged_feed(iidx_news_data, sdvx_news_data, chunithm_jp_news_data)
    with open(OUTPUT_DIR+'/news.json', 'w') as json_file:
        json.dump(attach_news_meta_data(news), json_file)
