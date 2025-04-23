from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import time
import re

def parse_museca_plus_news_site(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    news_posts = []
    base_url = "https://museca.plus/"
    for p in soup.select("div.subcontainer.center.text > p"):
        text = p.get_text(strip=True, separator=' ')
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
        if not date_match:
            continue
        date_str = date_match.group(1)
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            timestamp = int(time.mktime(dt.timetuple()))
        except ValueError:
            continue
        images = []
        for img in p.find_all("img"):
            img_url = urljoin(base_url, img.get("src"))
            parent_a = img.find_parent("a")
            images.append({"image": img_url, "link": None})

        content = p.get_text(separator=' ', strip=True)

        news_posts.append({
            'date': date_str,
            'identifier': 'MUSECA_PLUS',
            'type': None,
            'timestamp': timestamp,
            'headline': None,
            'content': content,
            'url': None,
            'images': images
        })

    return news_posts
