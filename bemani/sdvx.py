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
            'identifier': 'SOUND_VOLTEX',
            'type': None,
            'timestamp': timestamp,
            'headline': headline_text,
            'content': content,
            "url": None,
            'images': images,
            'is_ai_summary': False
        })

    return entries

def parse_nabla_news_site(html: str):
    base_url = "https://p.eagate.573.jp"
    soup = BeautifulSoup(html, 'html.parser')
    news_list = soup.select('#news-inner ul.news li')

    entries = []
    for li in news_list:
        strong_tags = li.select('strong')
        if not strong_tags:
            continue

        date = strong_tags[0]
        date_str = date.text.strip()
        try:
            dt = datetime.strptime(date_str, "%Y.%m.%d")
            timestamp = int(dt.timestamp())
        except ValueError:
            timestamp = None

        headline_text = None
        if len(strong_tags) > 1:
            headline_text = strong_tags[1].text.strip()

        for tag in li.select('font, b, u, span'):
            tag.unwrap()

        content_parts = []
        for node in li.contents:
            if hasattr(node, 'name'):
                if node.name == 'strong':
                    continue
                elif node.name == 'br':
                    content_parts.append('\n')
                elif node.name == 'a' and 'link-text' in node.get('class', []):
                    content_parts.append(node.text.strip())
                elif node.name not in ['img']:  # Skip image tags for content
                    content_parts.append(node.get_text(strip=True))
            else:
                text = str(node).strip()
                if text and text not in [date_str, headline_text]:
                    content_parts.append(text)

        content = '\n'.join(filter(None, content_parts)).strip()

        images = []
        for img in li.select('img'):
            src = img.get('data-original') or img.get('src')
            if not src or (isinstance(src, str) and src.startswith('data:')):
                continue
            if isinstance(src, str):
                src = urljoin(base_url, src)
                parent = img.find_parent('a')
                href = None
                if parent and hasattr(parent, 'get') and parent.get('href'):
                    href_val = parent.get('href')
                    if isinstance(href_val, str):
                        href = urljoin(base_url, href_val)

                image_entry = {'image': src, 'link': href}
                if image_entry not in images:
                    images.append(image_entry)

        entries.append({
            'date': date_str,
            'identifier': 'SOUND_VOLTEX',
            'type': None,
            'timestamp': timestamp,
            'headline': headline_text,
            'content': content,
            "url": None,
            'images': images,
            'is_ai_summary': False
        })

    return entries
