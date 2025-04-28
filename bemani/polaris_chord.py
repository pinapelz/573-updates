from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re

CATEGORY_MAP = {
    "i_01": "NEWS",
    "i_02": "MUSIC",
    "i_03": "EVENT",
    "i_04": "OTHER"
}


def parse_polaris_chord_news_site(html: str) -> list[dict]:
    soup = BeautifulSoup(html, 'html.parser')
    news_list = []
    for li in soup.select('#info-news li.news'):
        raw_date = li.find('li', class_='news_date').text.strip()
        match = re.search(r'(\d{4}/\d{1,2}/\d{1,2})', raw_date)
        if not match:
            continue
        date_str = match.group(1)

        try:
            dt = datetime.strptime(date_str, '%Y/%m/%d')
        except ValueError:
            continue
        jst = pytz.timezone('Asia/Tokyo')
        dt_jst = jst.localize(dt)
        timestamp = int(dt_jst.timestamp())

        raw_type = li.get('data-category')
        post_type = CATEGORY_MAP.get(raw_type)

        headline = li.find('li', class_='news_title').text.strip()
        detail = li.find('li', class_='news_detail')
        content = detail.get_text(separator='\n').strip()

        first_a = detail.find('a', href=True)
        url = first_a['href'] if first_a else None

        images = []
        for img in detail.find_all('img'):
            img_url = img.get('src')
            link = None
            if img.parent.name == 'a' and img.parent.has_attr('href'):
                link = img.parent['href']
            images.append({'image': img_url, 'link': link})

        entry = {
            'date': date_str,
            'identifier': "POLARIS_CHORD",
            'type': post_type,
            'timestamp': timestamp,
            'headline': headline,
            'content': content,
            'url': url,
            'images': images,
            'is_ai_summary': False,
        }
        news_list.append(entry)
    return news_list
