from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
import re

def parse_maimaidx_jp_prism_plus_news_site(html: str):
    soup = BeautifulSoup(html, "html.parser")
    base_url = "https://info-maimai.sega.jp/"
    news_items = []

    news_boxes = soup.select(".maiPager-content .newsBox")
    for box in news_boxes:
        a_tag = box.select_one("a")
        url = urljoin(base_url, a_tag["href"]) if a_tag and a_tag.get("href") else None

        img_tag = box.select_one("img")
        image_url = urljoin(base_url, img_tag["src"]) if img_tag else None

        date_tag = box.select_one(".newsDate")
        raw_date = date_tag.get_text(strip=True) if date_tag else None

        jst = timezone(timedelta(hours=9))
        try:
            dt = datetime.strptime(raw_date.split(" ")[0], "%Y.%m.%d").replace(tzinfo=jst)
            timestamp = int(dt.timestamp())
        except:
            dt = None
            timestamp = 0

        content_tag = box.select_one(".newsLink")
        content = content_tag.get_text(strip=True) if content_tag else None
        news_items.append({
            "date": raw_date,
            "identifier": "MAIMAIDX_JPN_PRISM_PLUS",
            "type": None,
            "timestamp": timestamp,
            "headline": None,
            "content": content,
            "url": url,
            "images": [{
                "image": image_url,
                "link": url
            }] if image_url else []
        })

    return news_items
