import json
from bs4 import BeautifulSoup
import re
from datetime import datetime

def _parse_html_content(html: str):
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        parent = img.find_parent("a")
        image_info = {
            "image": img["src"],
            "link": parent["href"] if parent else None
        }
        images.append(image_info)
        img.decompose()
    for br in soup.find_all("br"):
        br.replace_with("\n\n")
    for a in soup.find_all("a"):
        text = a.get_text()
        href = a.get("href")
        if href:
            markdown = f"[{text}]({href})"
            a.replace_with(f" {markdown} ")
        else:
            a.unwrap()
            a.insert_after(" ")
    for tag in soup.find_all(True):
        tag.insert_after(" ")
        tag.unwrap()
    text = soup.get_text()
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text, images

def parse_music_diver_news_json(data_str: str):
    data = json.loads(data_str)
    if data["responseCode"] != 200:
        return []

    news_posts = []
    for post in data["response"]:
        content, images = _parse_html_content(post["content"])
        show_date = datetime.fromisoformat(post["show_start"].replace("Z", "+00:00"))
        jst_date = show_date.strftime("%Y-%m-%d")
        timestamp = int(show_date.timestamp())

        news_posts.append({
            "date": jst_date,
            "identifier": "MUSIC_DIVER",
            "type": None,
            "timestamp": timestamp,
            "headline": post["title"],
            "content": content,
            "url": None,
            "images": images
        })
    return news_posts
