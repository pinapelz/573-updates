from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
import time

def get_carousel_posts(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    base_url = "https://dxplus.chilundui.com/"
    carousel = soup.find('div', class_='carousel-inner')
    if not carousel:
        return []

    news_posts = []
    current_date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_unix_time = int(time.time())
    for item in carousel.find_all('div', class_='carousel-item'):
        img_tag = item.find('img')
        if img_tag and img_tag.get('src'):
            news_posts.append({
                "date": current_date_string,
                "identifier": "REFLEC_BEAT_DELUXE_PLUS",
                "type": None,
                "timestamp": current_unix_time,
                "url": None,
                "headline": None,
                "content": "[お知らせ] ANNOUNCEMENT FROM REFLECT BEAT DELUXE PLUS",
                "images": [{"image": urljoin(base_url, img_tag['src']), "link": None}],
                'is_ai_summary': False
            })
    return news_posts
