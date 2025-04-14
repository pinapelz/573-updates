"""
Generates news JSON files
"""
import news_feed as feed
import constants
import json
import os


OUTPUT_DIR = "news"

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    iidx_news_data = feed.get_news(constants.IIDX_PINKY_CRUSH_NEWS_SITE)
    with open(OUTPUT_DIR+'/iidx_news.json', 'w') as json_file:
        json.dump(iidx_news_data, json_file)

    sdvx_news_data = feed.get_news(constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE)
    with open(OUTPUT_DIR+'/sdvx_news.json', 'w') as json_file:
        json.dump(sdvx_news_data, json_file)

    chunithm_jp_news_data = feed.get_news(constants.CHUNITHM_NEWS_SITE, constants.CHUNITHM_VERSION.VERSE)
    with open(OUTPUT_DIR+'/chunithm_jp_news.json', 'w') as json_file:
        json.dump(chunithm_jp_news_data, json_file)
