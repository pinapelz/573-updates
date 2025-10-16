from bs4 import BeautifulSoup
from datetime import datetime
import pytz
from urllib.parse import urljoin
import re

CATEGORY_MAP = {
    "i_01": "NEWS",
    "i_02": "MUSIC",
    "i_03": "EVENT",
    "i_04": "OTHER"
}

def parse_polaris_chord_news_site(html: str) -> list[dict]:
    base_url = "https://eacache.s.konaminet.jp/game/polarischord/pc/"
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []

    for li in soup.select('li.news'):
        raw_type = li.get('data-category')
        post_type = CATEGORY_MAP.get(raw_type, "OTHER")

        # Attempt to extract date from data-date (format: 20251015-01)
        raw_date = li.get('data-date', '')
        # Extract first 8 digits: YYYYMMDD
        if len(raw_date) < 8:
            continue
        date_part = raw_date[:8]
        date_match = re.match(r'(\d{4})(\d{2})(\d{2})', date_part)
        if not date_match:
            continue
        year, month, day = map(int, date_match.groups())
        if month < 1 or month > 12:
            continue
        if day < 1 or day > 31:
            continue
        if month in [4, 6, 9, 11] and day > 30:
            continue
        if month == 2 and day > 29:
            continue

        date_str = f"{year}/{month:02}/{day:02}"

        try:
            jst = pytz.timezone('Asia/Tokyo')
            dt_jst = jst.localize(datetime(year, month, day))
            timestamp = int(dt_jst.timestamp())
        except (ValueError, OverflowError):
            # Skip if datetime creation fails
            continue

        # Find the news-main ul inside the li
        news_main = li.find('ul', class_='news-main')
        if not news_main:
            continue

        # Extract headline from news_title li
        headline_li = news_main.find('li', class_='news_title')
        headline_text = headline_li.get_text(strip=True) if headline_li else None

        # Extract content from news_detail li
        detail_li = news_main.find('li', class_='news_detail')
        content = detail_li.get_text(strip=True) if detail_li else None

        # Find all images in the detail section
        images = []
        if detail_li:
            for img in detail_li.find_all('img'):
                # Check both src and data-src (for lazy loaded images)
                img_url = img.get('src') or img.get('data-src')
                if img_url and not img_url.startswith('http'):
                    img_url = urljoin(base_url, img_url)
                if img_url:
                    images.append({'image': img_url, 'link': None})

        entry = {
            'date': date_str,
            'identifier': "POLARIS_CHORD",
            'type': post_type,
            'timestamp': timestamp,
            'headline': headline_text,
            'content': content,
            'url': None,
            'images': images,
            'is_ai_summary': False,
        }
        news_list.append(entry)

    return news_list
