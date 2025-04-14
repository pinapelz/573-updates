from bs4 import BeautifulSoup
from datetime import datetime
import time

def parse_ongeki_refresh_news_site(html: str):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    for li in soup.select("li.p-news__listChild"):
        a_tag = li.select_one("a.p-news__listLink")
        url = a_tag["href"] if a_tag else None

        img_tag = li.select_one(".p-news__listThumb img")
        image_url = img_tag["src"] if img_tag else None
        image_alt = img_tag["alt"] if img_tag else ""
        image_link = url if image_url else None

        date_type_text = li.select_one(".p-news__listTextUpper")
        date_text = date_type_text.text.strip().split("/")[0].strip() if date_type_text else None
        type_text = date_type_text.text.strip().split("/")[-1].strip() if "/" in date_type_text.text else None

        headline_tag = li.select_one(".p-news__listTextUnder")
        headline = headline_tag.text.strip() if headline_tag else None

        timestamp = None
        if date_text:
            try:
                dt = datetime.strptime(date_text, "%Y.%m.%d %a")
                timestamp = int(time.mktime(dt.timetuple()))
            except:
                timestamp = None
        entry = {
            "date": date_text,
            "identifier": "ONGEKI_JPN_REFRESH",
            "type": type_text if type_text not in ["GAME", "CARDMAKER"] else None,
            "timestamp": timestamp,
            "headline": None,
            "content": image_alt,
            "url": url,
            "images": [{
                "image": image_url,
                "link": image_link
            }] if image_url else []
        }

        items.append(entry)

    return items
