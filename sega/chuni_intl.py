from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
import re
from enum import Enum

class ParserVersion(Enum):
    ALPHA=1

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

            results.append({
                "date": dt.strftime("%Y-%m-%d"),
                "identifier": identifier,
                "type": None,
                "timestamp": timestamp,
                "headline": None,
                "content": headline,
                "url": url,
                "images": [{
                    "image": image_url,
                    "link": url
                }] if image_url else []
            })

        return results

    if parser == ParserVersion.ALPHA:
        return alpha_parser

parse_chuni_intl_luminous_plus_news_site = make_chuni_intl_parser("CHUNITHM_INTL_LUMINOUS_PLUS", ParserVersion.ALPHA)
