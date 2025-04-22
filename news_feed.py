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
    'images': [
    {
        'image': URL to image,
        'link': If there's an associated href. Else None
        }

    ]
}
"""

from site_scraper import SiteScraper, download_site_as_html
import konami.eamuse_app as eamuse_app
import bemani.sdvx as sound_voltex
import bemani.iidx as iidx
import bemani.ddr as ddr
import sega.chuni_jp as chunithm_jp
import sega.chuni_intl as chuni_intl
import sega.maimaidx_jp as maimaidx_jp
import sega.maimaidx_intl as maimaidx_intl
import sega.ongeki_jp as ongeki_jp
import taito.music_diver as music_diver
import bandai_namco.taiko as taiko
import community.disc as disc
import community.wacca_plus.wacca_plus as wac_plus
import constants
import translate

def get_news(news_url: str, version=None) -> list:
    if news_url == constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(sound_voltex.parse_exceed_gear_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.IIDX_PINKY_CRUSH_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(iidx.parse_pinky_crush_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts, iidx.KEY_TERMS_TL)

    elif news_url == constants.EAMUSE_APP_FEED:
        scraper = SiteScraper(headless=True)
        site_data = scraper.get_page_source(news_url+"/?uuid_to="+version)
        scraper.close()
        match version:
            case constants.IIDX_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "IIDX_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts, iidx.KEY_TERMS_TL)
            case constants.DDR_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "DDR_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.SDVX_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "SOUND_VOLTEX_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.JUBEAT_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "JUBEAT_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.POPN_MUSIC_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "POPN_MUSIC_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.GITADORA_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "GITADORA_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.NOSTALGIA_EAMUSE_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "NOSTALGIA_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case _:
                raise ValueError("Cannot find provided e-amuse app gameId", version)

    elif news_url == constants.DDR_WORLD_NEWS_SITE:
        scraper = SiteScraper(headless=True)
        site_data = scraper.get_page_source(news_url)
        scraper.close()
        news_posts = sorted(ddr.parse_ddr_world_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.CHUNITHM_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.CHUNITHM_VERSION.VERSE:
            news_posts = sorted(chunithm_jp.parse_chuni_jp_verse_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
            news_posts = translate.add_translate_text_to_en(news_posts)
            if constants.CHUNI_RECURSIVE_IMAGE:
                for i in range(len(news_posts)):
                    if not news_posts[i]["url"]:
                        continue
                    post_site_data = download_site_as_html(news_posts[i]["url"])
                    post_images = chunithm_jp.parse_chuni_jp_verse_post_images(post_site_data)
                    news_posts[i]["images"].extend([image for image in post_images if not any(existing_image['image'] == image['image'] for existing_image in news_posts[i]["images"])])

    elif news_url == constants.CHUNITHM_INTL_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.CHUNITHM_VERSION.LUMINOUS_PLUS:
            news_posts = sorted(chuni_intl.parse_chuni_intl_luminous_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        elif version == constants.CHUNITHM_VERSION.VERSE:
            news_posts = sorted(chuni_intl.parse_chuni_intl_verse_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
            if constants.CHUNI_RECURSIVE_IMAGE:
                for i in range(len(news_posts)):
                    if not news_posts[i]["url"]:
                        continue
                    post_site_data = download_site_as_html(news_posts[i]["url"])
                    post_images = chuni_intl.parse_chuni_intl_verse_post_images(post_site_data)
                    news_posts[i]["images"].extend([image for image in post_images if not any(existing_image['image'] == image['image'] for existing_image in news_posts[i]["images"])])


    elif news_url == constants.MAIMAIDX_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.MAIMAIDX_VERSION.PRISM_PLUS:
            news_posts = sorted(maimaidx_jp.parse_maimaidx_jp_prism_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
            news_posts = translate.add_translate_text_to_en(news_posts)

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
            news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.MUSIC_DIVER_NEWS:
        api_data = download_site_as_html(news_url)
        news_posts = sorted(music_diver.parse_music_diver_news_json(api_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.TAIKO_BLOG_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(taiko.parse_taiko_blog_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.WACCA_PLUS_MAGIC_STRING:
        if not wac_plus.check_is_generation_possible():
            news_posts = []
        else:
            messages = disc.fetch_messages(constants.WACCA_PLUS_MAGIC_STRING)
            news_posts = sorted(wac_plus.parse_announcement_messages(messages), key=lambda x: x['timestamp'], reverse=True)
    else:
        news_posts = []
    return news_posts
