from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
import re


def parse_pinky_crush_news_site(html: str, base_url):
    type_map = {
        "i_01": "NEWSONG",
        "i_02": "RANKING",
        "i_03": "EVENT",
        "i_04": "SHOP",
        "i_05": "OTHER"
    }
    soup = BeautifulSoup(html, "html.parser")
    news_items = []

    for li in soup.select("#info-news > li"):
        date_elem = li.select_one(".news-main > li:nth-of-type(1)")
        headline_elem = li.select_one(".news-main > li:nth-of-type(2)")
        content_elem = li.select_one(".news-main > li:nth-of-type(3)")
        type_class = li.get("class", [None])[0]
        if not (date_elem and content_elem):
            continue
        date_str = date_elem.text.strip()
        try:
            dt = datetime.strptime(date_str, "%Y/%m/%d")
            timestamp = int(dt.timestamp())
        except ValueError:
            timestamp = None

        headline = headline_elem.a.text.strip() if headline_elem.a else headline_elem.text.strip()

        for a in content_elem.select("a[href]"):
            href = urljoin(base_url, a["href"])
            text = a.get_text(strip=True)
            a.replace_with(f"[{text}]({href})")

        for br in content_elem.find_all("br"):
            br.replace_with("\n")

        content = content_elem.get_text().strip()

        content = content.replace(
            "                              e-amusement ベーシックコース                          ",
            " e-amusement ベーシックコース "
        )
        content = content.replace("※", "\n※")
        content = re.sub(r"\n[ \t]+", "\n", content)
        content = re.sub(r'\s*/\s*', '/', content)
        news_items.append({
            "date": date_str,
            "type": type_map[type_class],
            "timestamp": timestamp,
            "headline": headline,
            "content": content,
            "url": None,
            "images": [],
        })

    return news_items
