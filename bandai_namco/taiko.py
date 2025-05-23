from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

def parse_taiko_blog_site(html: str) -> list:
    base_url: str = "https://taiko-ch.net"
    soup = BeautifulSoup(html, "html.parser")

    entries = []

    for article in soup.select("article"):
        try:
            # Get date and timestamp
            date_tag = article.select_one("p.entryDate")
            if not date_tag:
                continue
            date_str = date_tag.text.strip()
            date_obj = datetime.strptime(date_str, "%Y年%m月%d日")
            timestamp = int(time.mktime(date_obj.timetuple()))
            url_date = date_obj.strftime("%Y%m%d")
            url = base_url + "/blog/?m="+url_date

            # Get headline
            headline_tag = article.select_one("h1")
            headline = headline_tag.text.strip() if headline_tag else None

            # Get subheaders
            content = []
            for div in article.find_all("div", style=re.compile(r"background:\s?#ff4500")):
                title_text = div.get_text(strip=True).replace("■", "").strip()
                if title_text:
                    content.append(f"• {title_text}")

            # Get images
            images = []
            for img in article.find_all("img"):
                img_url = img.get("src") or img.get("data-src")
                if img_url:
                    if img_url.startswith("/"):
                        img_url = base_url + img_url
                    images.append({"image": img_url, "link": None})

            entry = {
                "date": date_str,
                "identifier": "TAIKO",
                "type": None,
                "timestamp": timestamp,
                "headline": headline,
                "content": "\n".join(content),
                "url": url,
                "images": images,
                'is_ai_summary': False
            }

            entries.append(entry)
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue

    return entries
