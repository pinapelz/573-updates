from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from enum import Enum

class ParserVersion(Enum):
    ALPHA=1

def make_maimaidx_intl_parser(identifier: str, parser: ParserVersion):
    def alpha_parser(html: str):
        """
        Confirmed on:
        PRISM
        """
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select(".dl--pop__item")

        entries = []
        for item in items:
            date_text = item.select_one(".dl--pop__head").text.strip().replace(" UP", "")
            dt = datetime.strptime(date_text, "%Y.%m.%d").replace(tzinfo=timezone(timedelta(hours=9)))
            timestamp = int(dt.timestamp())

            img_tag = item.select_one("a.dl--pop__thumb img")
            image_url = img_tag["srcset"] if img_tag else None
            full_image_url = image_url.replace("../", "https://maimai.sega.com/") if image_url else None

            entry = {
                "date": date_text,
                "identifier": identifier,
                "type": None,
                "timestamp": timestamp,
                "headline": None,
                "content": f"New maimai DX International News / maimai DX International の新しいお知らせ\n\n{full_image_url}",
                "url": None,
                "images": [
                    {
                        "image": full_image_url,
                        "link": None
                    }
                ]
            }
            entries.append(entry)
        return entries
    if parser == ParserVersion.ALPHA:
        return alpha_parser

parse_maimaidx_intl_prism_news_site = make_maimaidx_intl_parser("MAIMAIDX_INTL_PRISM", ParserVersion.ALPHA)
