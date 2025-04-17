from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import time
import re

def parse_ddr_world_news_site(html: str):
    base_url = "https://p.eagate.573.jp"
    soup = BeautifulSoup(html, 'html.parser')
    news_entries = []

    for div in soup.select("div#info > div.news_one"):
        if 'none' in div.get('style', ''):
            continue
        title_tag = div.select_one("div.news_title > div.title")
        date_tag  = div.select_one("div.news_title > div.date")
        headline  = title_tag.get_text(strip=True) if title_tag else None
        date_str  = date_tag.get_text(strip=True)  if date_tag  else None

        try:
            dt = datetime.strptime(date_str, "%Y/%m/%d")
            date_iso  = dt.strftime("%Y-%m-%d")
            timestamp = int(time.mktime(dt.timetuple()))
        except Exception:
            date_iso, timestamp = None, None

        paras = [p.get_text(strip=True, separator="\n")
                 for p in div.find_all("p", recursive=False)]
        if not paras:
            for child in div.find_all(recursive=False):
                cls = child.get("class", [])
                if "news_title" in cls or "img_news_center" in cls:
                    continue
                if child.name == "div":
                    paras.append(child.get_text(strip=True, separator="\n"))
        content = "\n\n".join(paras) if paras else None

        # image (use data-src if present)
        img = div.select_one("div.img_news_center img")
        raw_src = img.get("data-src") or img.get("src") if img else None
        image_url = urljoin(base_url, raw_src) if raw_src else None

        news_entries.append({
            "date":       date_iso,
            "identifier": "DDR_WORLD",
            "type":       None,
            "timestamp":  timestamp,
            "headline":   headline,
            "content":    content,
            "url":        base_url,
            "images": {
                "image": image_url,
                "link":  None
            }
        })
    return news_entries
