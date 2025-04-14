from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from urllib.parse import urljoin
import re

def parse_chuni_jp_verse_news_site(html: str):
    soup = BeautifulSoup(html, "html.parser")
    news_entries = []
    news_wrapper = soup.find("div", class_="newsMainWrapper-left")
    if not news_wrapper:
        return news_entries
    for a_tag in news_wrapper.find_all("a", href=True):
        if not a_tag.find("div", class_="chuniCommonBox-inner"):
            continue
        news_dict = {}
        news_url = a_tag.get("href")
        news_dict["url"] = news_url
        date_container = a_tag.find("div", class_="chuniCommonBox-inner-title")
        date_str = None
        if date_container:
            title_span = date_container.find("span", class_="title")
            if title_span:
                text = title_span.get_text(strip=True)
                date_match = re.search(r"(\d{4}\.\d{2}\.\d{2})", text)
                if date_match:
                    date_str = date_match.group(1)
        news_dict["date"] = date_str
        news_dict["type"] = None
        timestamp = None
        if date_str:
            try:
                dt = datetime.strptime(date_str, "%Y.%m.%d")
                dt = dt.replace(tzinfo=timezone(timedelta(hours=9)))
                timestamp = int(dt.timestamp())
            except Exception:
                timestamp = None
        news_dict["timestamp"] = timestamp
        main_content = a_tag.find("div", class_="chuniCommonBox-inner-main")
        headline = None
        content_text = ""
        if main_content:
            img_tag = main_content.find("img")
            if img_tag and img_tag.get("alt"):
                headline = img_tag.get("alt")
            else:
                headline = main_content.get_text(separator=" ", strip=True)
            content_text = main_content.get_text(separator=" ", strip=True)
        news_dict["headline"] = headline
        news_dict["content"] = content_text
        images = {"image": None, "link": None}
        if main_content:
            img_tag = main_content.find("img")
            if img_tag:
                images["image"] = img_tag.get("src")
                images["link"] = news_url
        news_dict["images"] = [images]
        news_dict["identifier"] = "CHUNITHM_JP_VERSE"

        news_entries.append(news_dict)

    return news_entries
