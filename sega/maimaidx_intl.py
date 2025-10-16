from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from enum import Enum
import json

class ParserVersion(Enum):
    ALPHA=1

def make_maimaidx_intl_parser(identifier: str, parser: ParserVersion):
    """
    Parses the download page of maimai dx intl site. API route method below is preferred as information is the same
    """
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
                ],
                'is_ai_summary': False
            }
            entries.append(entry)
        return entries
    if parser == ParserVersion.ALPHA:
        return alpha_parser

def parse_maimaidx_intl_api_route(raw_api_data: str, identifier: str, limit: int):
    route_data = json.loads(raw_api_data)
    route_data = route_data[:limit]
    entries = []
    for post_data in route_data:
        date_data = post_data["date"]
        date_str = ".".join([str(x) for x in date_data[:3]]) # YYYY.MM.DD
        dt = datetime.strptime(date_str, "%Y.%m.%d").replace(tzinfo=timezone(timedelta(hours=9)))
        timestamp = int(dt.timestamp())
        full_image_url = f"https://maimai.sega.com/assets/img/download/pop/download/{date_data[0]}-{date_data[1]}-{date_data[2]}/{post_data['thumb']}"
        if len(date_data) == 4:
            full_image_url = f"https://maimai.sega.com/assets/img/download/pop/download/{date_data[0]}-{date_data[1]}-{date_data[2]}-{date_data[3]}/{post_data['thumb']}"
        content = post_data["desc"] + f"\n\nNew maimai DX International News / maimai DX International の新しいお知らせ\n\n{full_image_url}"
        headline = post_data["title"]
        images = [{
            "image": full_image_url,
            "link": None
        }]
        entry = {
            "date": date_str,
            "identifier": identifier,
            "type": None,
            "timestamp": timestamp,
            "headline": headline,
            "content": content,
            "url": None,
            "images": images,
            "is_ai_summary": False
        }
        entries.append(entry)
    return entries


parse_maimaidx_intl_news_site = make_maimaidx_intl_parser("MAIMAIDX_INTL", ParserVersion.ALPHA)
