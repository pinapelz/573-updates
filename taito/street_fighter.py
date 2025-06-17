import json
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urljoin
from enum import Enum
from constants import STREET_FIGHTER_NEWS_SITE

class ParserVersion(Enum):
    ALPHA = 1

def make_sf_parser(identifier: str, parser: ParserVersion):
    def alpha_parser(html: str):
        soup = BeautifulSoup(html, "html.parser")
        news_entries = []
        news_links = soup.find_all('a', class_='btn_latestnews')
        for link in news_links:
            try:
                url = link.get('href', '')
                if url.startswith('/'):
                    url = urljoin(STREET_FIGHTER_NEWS_SITE, url)
                info_p = link.find('p', class_='info_list_event')
                if not info_p:
                    continue
                date_span = info_p.find('span', class_='latestnews_date')
                if not date_span:
                    continue
                date_text = date_span.get_text(strip=True)
                date_match = re.match(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*　(.+)', date_text)
                if not date_match:
                    continue
                date_str = date_match.group(1)
                time_str = date_match.group(2)
                datetime_str = f"{date_str} {time_str}"
                try:
                    post_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                    timestamp = int(post_date.timestamp())
                except ValueError:
                    continue
                headline_span = info_p.find('span', class_='info_list_txt')
                headline = headline_span.get_text(strip=True) if headline_span else ""
                headline = re.sub(r'<br\s*/?>', ' ', headline)
                headline = re.sub(r'\s+', ' ', headline).strip()
                images = []
                img_div = link.find('div', class_='image')
                if img_div:
                    img_tag = img_div.find('img')
                    if img_tag:
                        img_src = img_tag.get('src', '')
                        if img_src.startswith('/'):
                            img_src = urljoin('https://sf6ta.jp', img_src)
                        images.append({
                            'image': img_src,
                            'link': url
                        })
                news_entry = {
                    'date': post_date.strftime("%Y-%m-%d %H:%M"),
                    'identifier': identifier,
                    'type': None,
                    'timestamp': timestamp,
                    'headline': None,
                    'content': headline, # content should be prio-ed over headline
                    'url': url,
                    'images': images,
                    'is_ai_summary': False
                }
                news_entries.append(news_entry)

            except Exception as e:
                continue

        return news_entries

    if parser == ParserVersion.ALPHA:
        return alpha_parser
    else:
        raise ValueError("Unknown Parser Version")


parse_sf_news_site = make_sf_parser(
    "STREET_FIGHTER", ParserVersion.ALPHA
)
