from dotenv import load_dotenv
import requests
import constants
import re
import os
import json
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

def _load_translation_cache() -> list:
    cache_file = "tl_cache.json"
    tl_map = {}
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as file:
            entries = json.load(file)
            for entry in entries:
                key = hashlib.sha256((entry["source_lang"] + entry["target_lang"] + entry["source_txt"]).encode('utf-8')).hexdigest()
                tl_map[key] = entry["result_txt"]
            return tl_map
    else:
        with open(cache_file, "w", encoding="utf-8") as file:
            json.dump([], file, ensure_ascii=False, indent=4)
        return {}

def _add_to_translation_cache(source_lang: str, target_lang: str, source_txt: str, result_txt: str) -> None:
    cache_file = "tl_cache.json"
    cache_entry = {
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_txt": source_txt,
        "result_txt": result_txt
    }
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as file:
            cache = json.load(file)
    else:
        cache = []
    cache.append(cache_entry)
    with open(cache_file, "w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=4)

def request_google_translate(text: str, source: str="ja", target="en", translation_cache=None) -> tuple:
    """
    Translates input text and returns the translated text using Google Cloud Translation API.
    """
    key = hashlib.sha256((source + target + text).encode('utf-8')).hexdigest()
    if translation_cache and key in translation_cache:
        return translation_cache[key]
    API_KEY = os.getenv("GOOGLE_TRANSLATE_API_KEY")
    encoded_text, restore_data = _encode_links(text)
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text",
        "key": API_KEY,
    }
    response = requests.post(url, params=params)
    data = response.json()
    translated_text = data["data"]["translations"][0]["translatedText"]
    translation_cache[key] = translated_text
    _add_to_translation_cache(source, target, text, translated_text)
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
    translation_cache = _load_translation_cache()
    for post in news_post:
        headline = post.get("headline")
        if headline:
            for override in overrides:
                headline = headline.replace(override[0], override[1])
            post["en_headline"] = request_google_translate(headline, translation_cache=translation_cache)
        else:
            post["en_headline"] = None
        content = post.get("content")
        if content:
            for override in overrides:
                content = content.replace(override[0], override[1])
            en_content = request_google_translate(content, translation_cache=translation_cache)
            post["en_content"] = en_content
        else:
            post["en_content"] = None
        translated_posts.append(post)
    return translated_posts
