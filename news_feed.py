"""
Generic format for a news entry. All keys are considered to be nullable
{
    'date': JST date of news post,
    'identifier': unique identifier for the game (usually some deriv. of the title),
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

from site_scraper import SiteScraper, download_site_as_html
import bemani.sdvx as sound_voltex
import bemani.iidx as iidx
import sega.chuni_jp as chunithm_jp
import sega.chuni_intl as chuni_intl
import sega.maimaidx_jp as maimaidx_jp
import sega.maimaidx_intl as maimaidx_intl
import sega.ongeki_jp as ongeki_jp
import constants
import translate

def get_news(news_url: str, version=None) -> list:
    if news_url == constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(sound_voltex.parse_exceed_gear_news_site(site_data, constants.EAMUSEMENT_BASE_URL), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.IIDX_PINKY_CRUSH_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(iidx.parse_pinky_crush_news_site(site_data, constants.EAMUSEMENT_BASE_URL), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.CHUNITHM_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.CHUNITHM_VERSION.VERSE:
            news_posts = sorted(chunithm_jp.parse_chuni_jp_verse_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.CHUNITHM_INTL_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.CHUNITHM_VERSION.LUMINOUS_PLUS:
            news_posts = sorted(chuni_intl.parse_chuni_intl_luminous_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.MAIMAIDX_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.MAIMAIDX_VERSION.PRISM_PLUS:
            news_posts = sorted(maimaidx_jp.parse_maimaidx_jp_prism_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.MAIMAIDX_INTL_NEWS_SITE:
        scraper = SiteScraper(headless=True)
        site_data = scraper.get_page_source(news_url)
        scraper.close()
        if version == constants.MAIMAIDX_VERSION.PRISM:
            news_posts = sorted(maimaidx_intl.parse_maimaidx_intl_prism_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.ONGEKI_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.ONGEKI_VERSION.REFRESH:
            news_posts = sorted(ongeki_jp.parse_ongeki_refresh_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
    else:
        news_posts = []
    return news_posts
