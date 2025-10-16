from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin


def parse_idac_news_site(site_data: str):
    soup = BeautifulSoup(site_data, "html.parser")
    news_entries = []
    articles = soup.find_all('article', class_=lambda x: x and 'post-' in x)
    for article in articles:
        try:
            post_id = None
            for cls in article.get('class', []):
                if cls.startswith('post-') and cls[5:].isdigit():
                    post_id = cls[5:]
                    break

            if not post_id:
                continue
            title_section = article.find('h1', class_='entry-title')
            if not title_section:
                continue
            news_title_link = title_section.find('a', class_='news-title')
            if not news_title_link:
                continue

            url = news_title_link.get('href', '')
            headline = news_title_link.get_text(strip=True)
            date_span = title_section.find('span', class_='entry_date')
            if not date_span:
                continue

            date_text = date_span.get_text(strip=True)

            date_match = re.match(r'(\d{4})年(\d{1,2})月(\d{1,2})日', date_text)
            if not date_match:
                continue

            year = int(date_match.group(1))
            month = int(date_match.group(2))
            day = int(date_match.group(3))

            # Create datetime object (assuming JST timezone, noon time)
            try:
                post_date = datetime(year, month, day, 12, 0)
                timestamp = int(post_date.timestamp())
            except ValueError:
                continue
            post_type = None
            categories_list = title_section.find('ul', class_='post-categories')
            if categories_list:
                category_link = categories_list.find('a')
                if category_link:
                    post_type = category_link.get_text(strip=True)
            content = ""
            entry_summary = article.find('div', class_='entry-summary')
            if entry_summary:
                content = entry_summary.get_text(strip=True)
                content = re.sub(r'続きを読む\s*.*$', '', content).strip()
                content = re.sub(r'\s*…\s*$', '', content).strip()
            images = []
            img_tags = article.find_all('img')
            for img in img_tags:
                img_src = img.get('src', '')
                if img_src and not img_src.endswith('.svg'):  # Skip icon/UI images
                    if img_src.startswith('/'):
                        img_src = urljoin('https://info-initialdac.sega.jp', img_src)
                    images.append({
                        'image': img_src,
                        'link': url
                    })
            news_entry = {
                'date': post_date.strftime("%Y-%m-%d %H:%M"),
                'identifier': "IDAC_NEWS",
                'type': post_type,
                'timestamp': timestamp,
                'headline': headline,
                'content': content if content else headline,
                'url': url,
                'images': images,
                'is_ai_summary': False
            }

            news_entries.append(news_entry)

        except Exception as e:
            # Skip malformed entries
            continue

    return news_entries


def get_promo_image(site_data: str) -> str:
    soup = BeautifulSoup(site_data, "html.parser")
    entry_content = soup.find('div', class_='entry-content')
    if entry_content:
        img_tag = entry_content.find('img')
        if img_tag:
            return img_tag.get('src', '')
    return ''
