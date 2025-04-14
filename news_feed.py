"""
Generic format for a news entry. All keys are considered to be nullable
{
    'date': JST date of news post
    'type': Type of post if available, otherwise if not provided it will be None (aka Generic news)
    'timestamp': Unixtime of date above,
    'headline': Headline,
    'content': All text content of news,
    'url': URL to full post if available,
    'images': {
        'image': URL to image,
        'link': If there's an associated href. Else None

    }
}
"""

from email.utils import parsedate_to_datetime
from datetime import datetime
from site_scraper import SiteScraper
import bemani.sdvx as sound_voltex
import bemani.iidx as iidx
import sega.chuni_jp as chunithm_jp
import constants

def get_news(news_url: str, version=None) -> list:
    scraper = SiteScraper(headless=True)
    news_json = {}
    site_data = scraper.get_page_source(news_url)
    if news_url == constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE:
        news_posts = sorted(sound_voltex.parse_exceed_gear_news_site(site_data, constants.EAMUSEMENT_BASE_URL), key=lambda x: x['timestamp'], reverse=True)
    elif news_url == constants.IIDX_PINKY_CRUSH_NEWS_SITE:
        news_posts = sorted(iidx.parse_pinky_crush_news_site(site_data, constants.EAMUSEMENT_BASE_URL), key=lambda x: x['timestamp'], reverse=True)
    elif news_url == constants.CHUNITHM_NEWS_SITE:
        if version == constants.CHUNITHM_VERSION.VERSE:
            news_posts = sorted(chunithm_jp.parse_chuni_jp_verse_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
    else:
        news_posts = []
    scraper.close()
    news_json = {
        "fetch_date": int(datetime.now().timestamp()),
        "posts": news_posts

    }
    return news_json
