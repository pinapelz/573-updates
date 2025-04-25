import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ParserVersion(Enum):
    ALPHA = 1


def make_chuni_intl_parser(identifier: str, parser: ParserVersion):
    def alpha_parser(html: str):
        """
        Confirmed on:
        LUMINOUS PLUS
        """
        soup = BeautifulSoup(html, "html.parser")
        base_url = "https://info-chunithm.sega.com/"
        items = soup.select("li.news--list__item")
        results = []

        for item in items:
            a_tag = item.select_one("a.news--list__post")
            if not a_tag:
                continue

            url = urljoin(base_url, a_tag["href"])
            date_text = item.select_one("div.news--date").text.strip()
            headline = item.select_one("p.news--title").text.strip()
            img_tag = item.select_one("div.news--thumbnail img")
            image_url = urljoin(base_url, img_tag["src"]) if img_tag else None

            date_match = re.match(r"(\d{4})\.(\d{1,2})\.(\d{1,2})", date_text)
            if not date_match:
                continue
            year, month, day = map(int, date_match.groups())
            jst = timezone(timedelta(hours=9))
            dt = datetime(year, month, day, tzinfo=jst)
            timestamp = int(dt.timestamp())

            results.append(
                {
                    "date": dt.strftime("%Y-%m-%d"),
                    "identifier": identifier,
                    "type": None,
                    "timestamp": timestamp,
                    "headline": None,
                    "content": headline,
                    "url": url,
                    "images": [{"image": image_url, "link": url}] if image_url else [],
                    'is_ai_summary': False
                }
            )

        return results

    if parser == ParserVersion.ALPHA:
        return alpha_parser


def make_image_extractor(version: ParserVersion):
    """
    Gets all the images from a full post page as CHUNITHM intl has more relevant images
    hidden in the actual posts
    """

    def image_extractor_alpha(html: str):
        base_url = "https://info-chunithm.sega.com/"
        soup = BeautifulSoup(html, "html.parser")
        images = []
        news_post = soup.select_one(".news--post")
        if not news_post:
            return images

        for img in news_post.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if not src:
                continue

            full_url = urljoin(base_url, src)
            parent = img.find_parent("a")
            link = parent.get("href") if parent and parent.name == "a" else None

            images.append(
                {"image": full_url, "link": urljoin(base_url, link) if link else None}
            )

        return images

    if version == ParserVersion.ALPHA:
        return image_extractor_alpha
    else:
        raise ValueError("Unknown Parser Version")


parse_chuni_intl_luminous_plus_news_site = make_chuni_intl_parser(
    "CHUNITHM_INTL_LUMINOUS_PLUS", ParserVersion.ALPHA
)

parse_chuni_intl_verse_news_site = make_chuni_intl_parser(
    "CHUNITHM_INTL_VERSE", ParserVersion.ALPHA
)
parse_chuni_intl_verse_post_images = make_image_extractor(ParserVersion.ALPHA)
