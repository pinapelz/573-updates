import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class ParserVersion(Enum):
    ALPHA = 1


def make_chuni_jp_parser(identifier: str, parser: ParserVersion):
    def alpha_parser(html: str):
        """
        Confirmed on:
        VERSE
        """
        soup = BeautifulSoup(html, "html.parser")
        news_entries = []
        news_wrapper = soup.find("div", class_="newsMainWrapper-left")
        if not news_wrapper:
            return news_entries
        for a_tag in news_wrapper.find_all("a", href=True):
            if not a_tag.find("div", class_="chuniCommonBox-inner"):
                continue
            news_dict = {}
            news_url = a_tag.get("href")
            news_dict["url"] = news_url

            date_container = a_tag.find("div", class_="chuniCommonBox-inner-title")
            date_str = None
            if date_container:
                title_span = date_container.find("span", class_="title")
                if title_span:
                    text = title_span.get_text(strip=True)
                    date_match = re.search(r"(\d{4}\.\d{2}\.\d{2})", text)
                    if date_match:
                        date_str = date_match.group(1)
            news_dict["date"] = date_str
            news_dict["type"] = None
            timestamp = None
            if date_str:
                try:
                    dt = datetime.strptime(date_str, "%Y.%m.%d")
                    dt = dt.replace(tzinfo=timezone(timedelta(hours=9)))
                    timestamp = int(dt.timestamp())
                except Exception:
                    timestamp = None
            news_dict["timestamp"] = timestamp

            main_content = a_tag.find("div", class_="chuniCommonBox-inner-main")
            content_text = ""
            if main_content:
                content_text = main_content.get_text(separator=" ", strip=True)
            news_dict["content"] = content_text

            images = {"image": None, "link": None}
            if main_content:
                img_tag = main_content.find("img")
                if img_tag:
                    images["image"] = img_tag.get("src")
                    images["link"] = news_url
            news_dict["images"] = [images]
            news_dict["identifier"] = identifier

            news_entries.append(news_dict)

        return news_entries

    if parser == ParserVersion.ALPHA:
        return alpha_parser


def make_image_extractor(version: ParserVersion):
    """
    Gets all the images from a full post page as CHUNITHM intl has more relevant images
    hidden in the actual posts
    """

    def image_extractor_alpha(html: str):
        base_url = "https://info-chunithm.sega.jp/"
        soup = BeautifulSoup(html, "html.parser")
        images = []

        container = soup.select_one(".chuniCommonBox-inner-main")
        if not container:
            return images
        for img in container.find_all("img"):
            if img.find_parent("p") and "©" in img.find_parent("p").text:
                continue

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


parse_chuni_jp_verse_news_site = make_chuni_jp_parser(
    "CHUNITHM_JP_VERSE", ParserVersion.ALPHA
)
parse_chuni_jp_verse_post_images = make_image_extractor(ParserVersion.ALPHA)
