from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import json
import time

BASE_URL = "https://eam.573.jp"

def parse_news_page(html: str, identifier: str):
    """
    Legacy method of scraping. Should not be used if API method works since it will be much faster
    """
    soup = BeautifulSoup(html, "html.parser")
    entries = []

    for li in soup.select("ul > li.ef"):
        a_tag = li.find("a", href=True)
        url = urljoin(BASE_URL, a_tag["href"]) if a_tag else None

        date_text = li.select_one(".post-date")
        if not date_text:
            continue
        raw_date = date_text.get_text(strip=True).replace("年", "/").replace("月", "/").replace("日", "")
        try:
            date_obj = datetime.strptime(raw_date, "%Y/%m/%d")
        except ValueError:
            continue
        date_str = date_obj.strftime("%Y-%m-%d")
        timestamp = int(time.mktime(date_obj.timetuple()))

        content_tag = li.select_one(".article-text")
        content = content_tag.get_text(strip=True) if content_tag else None

        img_tag = li.select_one(".article-img img")
        image_url = img_tag["src"] if img_tag else None
        images = []
        if image_url:
            images.append({
                "image": image_url,
                "link": url
            })

        entry = {
            "date": date_str,
            "identifier": identifier,
            "type": None,
            "timestamp": timestamp,
            "headline": None,
            "content": content,
            "url": url,
            "images": images,
            'is_ai_summary': False
        }
        entries.append(entry)

    return entries

def parse_news_api_route(raw_api_data: str, identifier: str, eam_news_site: str=""):
    """
    Re-maps eamuse news app API routes to 573Updates JSON
    """
    route_data = json.loads(raw_api_data)
    entries = []
    for post_data in route_data["post_list"]:
        date_str = post_data["entry_date"]
        timestamp = post_data["entry_time"]
        content = post_data["content"]
        url = eam_news_site + "?post_id="+post_data["post_id"]
        images = []
        if "image_url" in post_data:
            images = [{
                "image": post_data["image_url"],
                "link": url
        }]
        entry = {
            "date": date_str,
            "identifier": identifier,
            "type": None,
            "timestamp": timestamp,
            "headline": None,
            "content": content,
            "url": url,
            "images": images,
            "is_ai_summary": False
        }
        entries.append(entry)
    return entries
