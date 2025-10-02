from dotenv import load_dotenv
from database import Database
import requests
import constants
import re
import os
import hashlib


load_dotenv()

def _encode_links(markdown_text: str) -> tuple:
    """
    Find all occurrences of markdown links, replace them with 573_UPDATE_MARKDOWN_LINK_N where N is the nth link,
    and record the word, its markdown replacement, and the occurrence count.
    """
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    links = []
    link_count = 0

    def replacer(match):
        nonlocal link_count
        link_count += 1
        markdown_replacement = match.group(0)
        placeholder = f"573_UPDATE_MARKDOWN_LINK_{link_count}"
        links.append((placeholder, markdown_replacement))
        return placeholder

    return link_pattern.sub(replacer, markdown_text), links

def _decode_links(raw_text: str, links: list) -> str:
    """
    Replaces the placeholders with hyperlinks
    """
    for link in links:
        raw_text = raw_text.replace(link[0], link[1])
    return raw_text

def request_google_translate(text: str, source: str="ja", target="en") -> tuple:
    """
    Translates input text and returns the translated text using Google Cloud Translation API.
    """
    key = hashlib.sha256((source + target + text).encode('utf-8')).hexdigest()
    database = Database()
    tl_result = database.get_translation(key)
    if tl_result:
        return tl_result
    API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    encoded_text, restore_data = _encode_links(text)
    url = "https://translation.googleapis.com/language/translate/v2?key="+API_KEY
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
    }
    response = requests.post(url, json=payload)
    data = response.json()
    translated_text = data["data"]["translations"][0]["translatedText"]
    database.add_new_translation(key=key, source_lang=source, target_lang=target, source_txt=text, result_txt=translated_text)
    database.close()
    return _decode_links(translated_text, restore_data)

def translation_possible() -> bool:
    return constants.ADD_EN_TRANSLATION and os.getenv("GOOGLE_TRANSLATE_API_KEY") is not None

def add_translate_text_to_en(news_post: dict, overrides: list=[]) -> dict:
    """
    Takes a news post dict as input, then appends the translated EN headline and content
    to the newspost and returns it
    """
    if not translation_possible():
        return news_post
    translated_posts = []
    for post in news_post:
        headline = post.get("headline")
        if headline:
            for override in overrides:
                headline = headline.replace(override[0], override[1])
            post["en_headline"] = request_google_translate(headline)
        else:
            post["en_headline"] = None
        content = post.get("content")
        if content:
            for override in overrides:
                content = content.replace(override[0], override[1])
            en_content = request_google_translate(content)
            post["en_content"] = en_content
        else:
            post["en_content"] = None
        translated_posts.append(post)
    return translated_posts
