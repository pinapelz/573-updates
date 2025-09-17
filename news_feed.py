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

    ],
    'is_ai_summary': boolean
}
"""

from site_scraper import SiteScraper, download_site_as_html
import konami.eamuse_app as eamuse_app
import bemani.sdvx as sound_voltex
import bemani.iidx as iidx
import bemani.ddr as ddr
import sega.chuni_jp as chunithm_jp
import bemani.polaris_chord as polaris_chord
import sega.chuni_intl as chuni_intl
import sega.maimaidx_jp as maimaidx_jp
import sega.maimaidx_intl as maimaidx_intl
import sega.ongeki_jp as ongeki_jp
import sega.idac as idac
import taito.music_diver as music_diver
import taito.street_fighter as street_fighter
import bandai_namco.taiko as taiko
import bandai_namco.wmmt as wmmt
import community.disc as disc
import community.wacca_plus.wacca_plus as wac_plus
import community.museca_plus as mus_plus
import community.rbdx as rbdx
import constants
import translate
import summarizer

from datetime import datetime

def _attach_llm_summaries(news_posts: list, game_name: str):
    for post in news_posts:
        image_urls = [img["image"] for img in post.get("images", []) if "image" in img]
        if image_urls:
            headline, content = summarizer.generate_headline_and_content_from_images(image_urls, game_name)
            if headline is None and content is None:
                datetime_str = datetime.now().strftime("%H:%M:%S")
                post["headline"] = f"{game_name} Update"
                post["content"] = f"573-UPDATES has found a news post for {game_name} at {datetime_str}, please refer to the image for more details!"
                post["is_ai_summary"] = False
            post["headline"] = headline
            post["content"] = content
            post["is_ai_summary"] = True


def get_news(news_url: str, version=None) -> list:
    if news_url == constants.SOUND_VOLTEX_EXCEED_GEAR_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(sound_voltex.parse_exceed_gear_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.IIDX_PINKY_CRUSH_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(iidx.parse_pinky_crush_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts, iidx.KEY_TERMS_TL)

    elif news_url == constants.POLARIS_CHORD_NEWS_SITE:
        scraper = SiteScraper(headless=True)
        site_data = scraper.get_page_source(news_url)
        news_posts = sorted(polaris_chord.parse_polaris_chord_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
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
            case constants.DANCE_RUSH_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "DANCE_RUSH_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
                news_posts = translate.add_translate_text_to_en(news_posts)
            case constants.DANCE_AROUND_APP_ID:
                news_posts= sorted(eamuse_app.parse_news_page(site_data, "DANCE_AROUND_EAMUSEMENT"), key=lambda x: x['timestamp'], reverse=True)
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
            _attach_llm_summaries(news_posts, "maimai DX International")

    elif news_url == constants.ONGEKI_JP_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        if version == constants.ONGEKI_VERSION.REFRESH:
            news_posts = sorted(ongeki_jp.parse_ongeki_refresh_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
            news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.IDAC_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(idac.parse_idac_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        for news in news_posts:
            promo_image_url = idac.get_promo_image(download_site_as_html(news["url"]))
            news["images"] = [{'image': promo_image_url, 'link': None}]
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.MUSIC_DIVER_NEWS:
        api_data = download_site_as_html(news_url)
        news_posts = sorted(music_diver.parse_music_diver_news_json(api_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.STREET_FIGHTER_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(street_fighter.parse_sf_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)


    elif news_url == constants.TAIKO_BLOG_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(taiko.parse_taiko_blog_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)

    elif news_url == constants.WANGAN_MAXI_GENERIC:
        news_posts = []
        na_site_data = download_site_as_html(constants.WANGAN_MAXI_NA_NEWS_SITE, response_encoding="utf-8")
        prelim_na_news_data = wmmt.get_wmmt_na_news_post_links(na_site_data)
        for data in prelim_na_news_data:
            post_site_data = download_site_as_html(data["url"])
            news = wmmt.parse_wmmt_na_news(post_site_data, data)
            if news is not None:
                news_posts.append(news)
        asia_oce_site_data = download_site_as_html(constants.WANGAN_MAXI_ASIA_OCE_NEWS_SITE, response_encoding="utf-8")
        prelim_asia_oce_news_data = wmmt.get_wmmt_asia_oce_news_post_links(asia_oce_site_data)
        for data in prelim_asia_oce_news_data:
            post_site_data = download_site_as_html(data["url"])
            news = wmmt.parse_wmmt_asia_oce_news(post_site_data, data)
            if news is not None:
                news_posts.append(news)
        jp_site_data = download_site_as_html(constants.WANGAN_MAXI_JP_NEWS_SITE, response_encoding="utf-8")
        prelim_jp_news_data = wmmt.get_wmmt_jp_news_post_links(jp_site_data)
        jp_news = []
        for data in prelim_jp_news_data:
            post_site_data = download_site_as_html(data["url"], response_encoding="utf-8")
            news = wmmt.parse_wmmt_jp_news(post_site_data, data)
            if news is not None:
                jp_news.append(news)
        jp_news = translate.add_translate_text_to_en(jp_news)
        news_posts.extend(jp_news)
        news_posts = sorted(news_posts, key=lambda x: x['timestamp'], reverse=True)
        return news_posts


    elif news_url == constants.WACCA_PLUS_MAGIC_STRING:
        if not wac_plus.check_is_generation_possible():
            news_posts = []
        else:
            messages = disc.fetch_messages(constants.WACCA_PLUS_MAGIC_STRING)
            news_posts = sorted(wac_plus.parse_announcement_messages(messages), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.MUSECA_PLUS_NEWS_SITE:
        site_data = download_site_as_html(news_url)
        news_posts = sorted(mus_plus.parse_museca_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)

    elif news_url == constants.RB_DELUXE_PLUS_NEWS:
        site_data = download_site_as_html(news_url)
        news_posts = rbdx.get_carousel_posts(site_data)
        _attach_llm_summaries(news_posts, "REFLEC BEAT PLUS DELUXE")

    else:
        news_posts = []
    return news_posts
