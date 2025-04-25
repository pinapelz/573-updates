from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def parse_exceed_gear_news_site(html: str):
    base_url = "https://p.eagate.573.jp"
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.select('.tab ul.news li')

    entries = []
    for li in news_list:
        date = li.select_one('strong')
        pre = li.select_one('pre')

        if not date or not pre:
            continue
        date_str = date.text.strip()
        try:
            dt = datetime.strptime(date_str, "%Y.%m.%d")
            timestamp = int(dt.timestamp())
        except ValueError:
            timestamp = None
        headline = li.select_one('p.notice')
        headline_text = headline.text.strip() if headline else None
        for tag in pre.select('font, b, u, span'):
            tag.unwrap()
        content = pre.get_text(separator='\n', strip=True)
        images = []
        for img in pre.select('img'):
            src = img.get('data-original') or img.get('src')
            if not src or src.startswith('data:'):
                continue
            src = urljoin(base_url, src)
            parent = img.find_parent('a')
            href = urljoin(base_url, parent['href']) if parent and parent.has_attr('href') else None
            if {'image': src, 'link': href} not in images:
                images.append({'image': src, 'link': href})

        entries.append({
            'date': date_str,
            'identifier': 'SOUND_VOLTEX_EXCEED_GEAR',
            'type': None,
            'timestamp': timestamp,
            'headline': headline_text,
            'content': content,
            "url": None,
            'images': images,
            'is_ai_summary': False
        })

    return entries
