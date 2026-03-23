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
from scrapers.base import NewsSource
import scrapers.registry as registry
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


# ---------------------------------------------------------------------------
# BEMANI (Specific feeds because these provide better information)
# ---------------------------------------------------------------------------

@registry.register(constants.SOUND_VOLTEX_NABLA_NEWS_SITE)
class SoundVoltexSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from bemani.sdvx import parse_nabla_news_site
        site_data = download_site_as_html(constants.SOUND_VOLTEX_NABLA_NEWS_SITE)
        news_posts = sorted(parse_nabla_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        return translate.add_translate_text_to_en(news_posts, overrides=[("ボルテ", "SDVX")])

# Can't find a Polaris feed on EAM app so this is here instead
@registry.register(constants.POLARIS_CHORD_NEWS_SITE)
class PolarisChordSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from bemani.polaris_chord import parse_polaris_chord_news_site
        site_data = download_site_as_html(constants.POLARIS_CHORD_NEWS_SITE)
        news_posts = sorted(
            parse_polaris_chord_news_site(site_data, constants.POLARIS_CHORD_RECENT_NEWS_LIMIT),
            key=lambda x: x['timestamp'],
            reverse=True,
        )
        return translate.add_translate_text_to_en(news_posts, overrides=[])


# ---------------------------------------------------------------------------
#  E-AMUSEMENT APP FEEDS (General Konami/BEMANI)
# ---------------------------------------------------------------------------

@registry.register(constants.EAMUSE_APP_API_ROUTE)
class EamuseAppSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from konami.eamuse_app import parse_news_api_route
        site_data = download_site_as_html(
            constants.EAMUSE_APP_API_ROUTE + "/?uuid_to=" + version + "&format=json"
        )
        match version:
            case constants.IIDX_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "IIDX_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.DDR_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "DDR_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.SDVX_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "SOUND_VOLTEX_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.JUBEAT_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "JUBEAT_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.POPN_MUSIC_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "POPN_MUSIC_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.GITADORA_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "GITADORA_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.NOSTALGIA_EAMUSE_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "NOSTALGIA_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.DANCE_RUSH_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "DANCE_RUSH_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case constants.DANCE_AROUND_APP_ID:
                news_posts = sorted(parse_news_api_route(site_data, "DANCE_AROUND_EAMUSEMENT", constants.EAMUSE_POST_SITE), key=lambda x: x['timestamp'], reverse=True)
                return translate.add_translate_text_to_en(news_posts)
            case _:
                raise ValueError("Cannot find provided e-amuse app gameId", version)

# ---------------------------------------------------------------------------
# SEGA
# ---------------------------------------------------------------------------

@registry.register(constants.CHUNITHM_JP_NEWS_SITE)
class ChunithmJPSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.chuni_jp import parse_chuni_jp_news_site, parse_chuni_jp_post_images
        site_data = download_site_as_html(constants.CHUNITHM_JP_NEWS_SITE)
        if version not in [constants.CHUNITHM_VERSION.VERSE, constants.CHUNITHM_VERSION.X_VERSE]:
            return []
        news_posts = sorted(parse_chuni_jp_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        news_posts = translate.add_translate_text_to_en(news_posts)
        if constants.CHUNI_RECURSIVE_IMAGE:
            for i in range(len(news_posts)):
                if not news_posts[i]["url"]:
                    continue
                post_site_data = download_site_as_html(news_posts[i]["url"])
                post_images = parse_chuni_jp_post_images(post_site_data)
                news_posts[i]["images"].extend([
                    image for image in post_images
                    if not any(existing["image"] == image["image"] for existing in news_posts[i]["images"])
                ])
        return news_posts


@registry.register(constants.CHUNITHM_INTL_NEWS_SITE)
class ChunithmIntlSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.chuni_intl import parse_chuni_intl_api_route, parse_chuni_intl_post_images
        site_data = download_site_as_html(constants.CHUNITHM_INTL_NEWS_SITE)
        news_posts = sorted(
            parse_chuni_intl_api_route(site_data, "CHUNITHM_INTL", constants.CHUNITHM_INTL_RECENT_NEWS_LIMIT),
            key=lambda x: x['timestamp'],
            reverse=True,
        )
        if constants.CHUNI_RECURSIVE_IMAGE:
            for i in range(len(news_posts)):
                if not news_posts[i]["url"]:
                    continue
                post_site_data = download_site_as_html(news_posts[i]["url"])
                post_images = parse_chuni_intl_post_images(post_site_data)
                news_posts[i]["images"].extend([
                    image for image in post_images
                    if not any(existing["image"] == image["image"] for existing in news_posts[i]["images"])
                ])
        return news_posts


@registry.register(constants.MAIMAIDX_JP_NEWS_SITE)
class MaimaiDXJPSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.maimaidx_jp import parse_maimaidx_jp_news_site
        site_data = download_site_as_html(constants.MAIMAIDX_JP_NEWS_SITE)
        if version not in [
            constants.MAIMAIDX_VERSION.PRISM_PLUS,
            constants.MAIMAIDX_VERSION.CIRCLE,
            constants.MAIMAIDX_VERSION.CIRCLE_PLUS,
        ]:
            return []
        news_posts = sorted(parse_maimaidx_jp_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        return translate.add_translate_text_to_en(news_posts)


@registry.register(constants.MAIMAIDX_INTL_NEWS_SITE)
class MaimaiDXIntlSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.maimaidx_intl import parse_maimaidx_intl_api_route
        site_data = download_site_as_html(constants.MAIMAIDX_INTL_NEWS_SITE)
        news_posts = sorted(
            parse_maimaidx_intl_api_route(site_data, "MAIMAIDX_INTL", constants.MAIMAIDX_INTL_RECENT_NEWS_LIMIT),
            key=lambda x: x['timestamp'],
            reverse=True,
        )
        _attach_llm_summaries(news_posts, "maimai DX International")
        return news_posts


@registry.register(constants.ONGEKI_JP_NEWS_SITE)
class OngekiJPSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.ongeki_jp import parse_ongeki_news_site
        site_data = download_site_as_html(constants.ONGEKI_JP_NEWS_SITE)
        if version != constants.ONGEKI_VERSION.REFRESH:
            return []
        news_posts = sorted(parse_ongeki_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        return translate.add_translate_text_to_en(news_posts)


@registry.register(constants.IDAC_NEWS_SITE)
class IDACSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from sega.idac import parse_idac_news_site, get_promo_image
        site_data = download_site_as_html(constants.IDAC_NEWS_SITE)
        news_posts = sorted(parse_idac_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        for news in news_posts:
            promo_image_url = get_promo_image(download_site_as_html(news["url"]))
            if promo_image_url.endswith("png") or promo_image_url.endswith("jpg"):
                news["images"] = [{'image': promo_image_url, 'link': None}]
            else:
                news["images"] = []
        return translate.add_translate_text_to_en(news_posts)


# ---------------------------------------------------------------------------
# Taito
# ---------------------------------------------------------------------------

@registry.register(constants.MUSIC_DIVER_NEWS)
class MusicDiverSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from taito.music_diver import parse_music_diver_news_json
        api_data = download_site_as_html(constants.MUSIC_DIVER_NEWS)
        return sorted(parse_music_diver_news_json(api_data), key=lambda x: x['timestamp'], reverse=True)


@registry.register(constants.STREET_FIGHTER_NEWS_SITE)
class StreetFighterSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from taito.street_fighter import parse_sf_news_site
        site_data = download_site_as_html(constants.STREET_FIGHTER_NEWS_SITE)
        news_posts = sorted(parse_sf_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        return translate.add_translate_text_to_en(news_posts)


# ---------------------------------------------------------------------------
# BANDAI NAMCO
# ---------------------------------------------------------------------------

@registry.register(constants.TAIKO_BLOG_SITE)
class TaikoBlogSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from bandai_namco.taiko import parse_taiko_blog_site
        site_data = download_site_as_html(constants.TAIKO_BLOG_SITE)
        news_posts = sorted(parse_taiko_blog_site(site_data), key=lambda x: x['timestamp'], reverse=True)
        return translate.add_translate_text_to_en(news_posts)


@registry.register(constants.WANGAN_MAXI_GENERIC)
class WanganMaxiSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from bandai_namco.wmmt import (
            get_wmmt_na_news_post_links,
            get_wmmt_asia_oce_news_post_links,
            get_wmmt_jp_news_post_links,
            parse_wmmt_na_news,
            parse_wmmt_asia_oce_news,
            parse_wmmt_jp_news,
        )
        news_posts = []

        na_site_data = download_site_as_html(constants.WANGAN_MAXI_NA_NEWS_SITE, response_encoding="utf-8")
        prelim_na_news_data = get_wmmt_na_news_post_links(na_site_data)
        for data in prelim_na_news_data:
            post_site_data = download_site_as_html(data["url"])
            news = parse_wmmt_na_news(post_site_data, data)
            if news is not None:
                news_posts.append(news)

        asia_oce_site_data = download_site_as_html(constants.WANGAN_MAXI_ASIA_OCE_NEWS_SITE, response_encoding="utf-8")
        prelim_asia_oce_news_data = get_wmmt_asia_oce_news_post_links(asia_oce_site_data)
        for data in prelim_asia_oce_news_data:
            post_site_data = download_site_as_html(data["url"])
            news = parse_wmmt_asia_oce_news(post_site_data, data)
            if news is not None:
                news_posts.append(news)

        jp_site_data = download_site_as_html(constants.WANGAN_MAXI_JP_NEWS_SITE, response_encoding="utf-8")
        prelim_jp_news_data = get_wmmt_jp_news_post_links(jp_site_data)
        jp_news = []
        for data in prelim_jp_news_data:
            post_site_data = download_site_as_html(data["url"], response_encoding="utf-8")
            news = parse_wmmt_jp_news(post_site_data, data)
            if news is not None:
                jp_news.append(news)
        jp_news = translate.add_translate_text_to_en(jp_news)
        news_posts.extend(jp_news)

        return sorted(news_posts, key=lambda x: x['timestamp'], reverse=True)


# ---------------------------------------------------------------------------
# Community
# ---------------------------------------------------------------------------

@registry.register(constants.WACCA_PLUS_MAGIC_STRING)
class WaccaPlusSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from community.wacca_plus import parse_announcement_messages, check_is_generation_possible
        from community.disc import fetch_messages
        if not check_is_generation_possible():
            return []
        messages = fetch_messages(constants.WACCA_PLUS_MAGIC_STRING)
        return sorted(parse_announcement_messages(messages), key=lambda x: x['timestamp'], reverse=True)


@registry.register(constants.MUSECA_PLUS_NEWS_SITE)
class MusecaPlusSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from community.museca_plus import parse_museca_plus_news_site
        site_data = download_site_as_html(constants.MUSECA_PLUS_NEWS_SITE)
        return sorted(parse_museca_plus_news_site(site_data), key=lambda x: x['timestamp'], reverse=True)


@registry.register(constants.RB_DELUXE_PLUS_NEWS)
class RBDeluxePlusSource(NewsSource):
    def fetch(self, version=None) -> list[dict]:
        from community.rbdx import get_carousel_posts
        site_data = download_site_as_html(constants.RB_DELUXE_PLUS_NEWS)
        news_posts = get_carousel_posts(site_data)
        _attach_llm_summaries(news_posts, "REFLEC BEAT PLUS DELUXE")
        return news_posts


def get_news(news_url: str, version=None) -> list[dict]:
    source_cls = registry.get_source(news_url)
    if source_cls is None:
        return []
    return source_cls().fetch(version)
