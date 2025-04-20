from bs4 import BeautifulSoup
from datetime import datetime
import time

def parse_changelog_to_news_format(html: str):
    soup = BeautifulSoup(html, "html.parser")
    news_items = []

    sections = soup.select("div.py-4")
    for section in sections:
        date_tag = section.find("h4")
        ul = section.find("ul")
        if not date_tag or not ul:
            continue

        date_str = date_tag.text.strip()
        try:
            date_obj = datetime.strptime(date_str, "%B %dth, %Y")
        except ValueError:
            try:
                date_obj = datetime.strptime(date_str, "%B %d, %Y")
            except ValueError:
                continue
        timestamp = int(time.mktime(date_obj.timetuple()))

        entries = [li.text.strip() for li in ul.find_all("li")]
        content = "\n".join(f"• {entry}" for entry in entries)

        news_item = {
            "date": date_str,
            "identifier": "MYT_NETWORK",
            "type": None,
            "timestamp": timestamp,
            "headline": f"MYT CHANGELOG ({date_str})",
            "content": content,
            "url": None,
            "images": []
        }
        news_items.append(news_item)

    return news_items
