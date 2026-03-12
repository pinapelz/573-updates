from datetime import datetime, timezone, timedelta

from bs4 import BeautifulSoup

JST = timezone(timedelta(hours=9))


def parse_ongeki_news_site(html: str):
    identifier = "ONGEKI_JPN"
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
        date_text = (
            date_type_text.text.strip().split("/")[0].strip()
            if date_type_text
            else None
        )
        type_text = (
            date_type_text.text.strip().split("/")[-1].strip()
            if date_type_text and "/" in date_type_text.text
            else None
        )

        timestamp = None
        if date_text:
            try:
                dt = datetime.strptime(date_text, "%Y.%m.%d %a").replace(tzinfo=JST)
                timestamp = int(dt.timestamp())
            except Exception:
                timestamp = None

        entry = {
            "date": date_text,
            "identifier": identifier,
            "type": type_text if type_text not in ["GAME", "CARDMAKER"] else None,
            "timestamp": timestamp,
            "headline": None,
            "content": image_alt,
            "url": url,
            "is_ai_summary": False,
            "images": [{"image": image_url, "link": image_link}]
            if image_url
            else [],
        }

        items.append(entry)

    return items