import re
from datetime import datetime, timedelta, timezone
from enum import Enum
from urllib.parse import urljoin
import sys
import os
import pytz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
import constants
from bs4 import BeautifulSoup

BASE_URL = "https://wanganmaxi-official.com"

TYPE_MAP = {
    "Online Events Information": "EVENTS",
    "Update Information": "UPDATE",
    "Future Lab News": "FUTURE LAB",
    "Special Contents": "SPECIAL",
    "Navi Scratch-off Item": "NAVI-SCRATCH",
    "News": "NEWS",
    "オンラインイベント情報": "EVENTS",
    "アップデート情報": "UPDATE",
    "未来研通信": "FUTURE LAB",
    "スペシャルコンテンツ": "SPECIAL",
    "ナビスクラッチ配信アイテム": "NAVI-SCRATCH",
    "ニュース": "NEWS"
}

def fix_image_url_path(base_url: str, image_path):
    if image_path.startswith("wanganmaxi"):
        from urllib.parse import urlparse
        parsed_url = urlparse(base_url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        return urljoin(domain, image_path)
    if base_url.endswith(".html"):
        base_url = re.sub(r"/[^/]+\.html$", "/", base_url)
    return urljoin(base_url, image_path.lstrip("/"))



def make_wmmt_parser(version: constants.WANGAN_MAXI_VERSION):
    def five_dx_plus_parser(html: str):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for section in soup.select("div.parts_column_02 > div.parts_bg_01"):
            type_heading = section.select_one("section h2.parts_txt_01")
            type_name = type_heading.get_text(strip=True) if type_heading else None
            count = 0
            for a in section.select("ul.archiveNav a[href]"):
                if count >= constants.WANGAN_MAXI_POSTS_PER_SECTION:
                    break
                href = a["href"]
                title_tag = a.find("h4")
                date_tag = a.find("p")
                title_parts = []
                for child in title_tag.children:
                    if child.name == "span":
                        title_parts.append(f"[{child.get_text(strip=True)}]")
                    elif isinstance(child, str):
                        title_parts.append(child.strip())
                title = " ".join(title_parts).strip()
                date = date_tag.get_text(strip=True) if date_tag else "No date"
                url = urljoin(BASE_URL, href)
                url = url.replace(".php", ".html")
                results.append({
                    "url": url,
                    "headline": title,
                    "date": date,
                    "type": TYPE_MAP.get(type_name, "Unknown")
                })
                count += 1
        return results

    def six_rr_parser(html: str):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for section in soup.select("div.parts_column_02 > div.parts_bg_01"):
            type_heading = section.select_one("section h2.parts_txt_01")
            type_name = type_heading.get_text(strip=True) if type_heading else None
            count = 0
            for a in section.select("ul.archiveNav a[href]"):
                if count >= constants.WANGAN_MAXI_POSTS_PER_SECTION:
                    break
                href = a["href"]
                date_tag = a.find("p")
                title_tag = a.find("h4")
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                date = date_tag.get_text(strip=True) if date_tag else "No date"
                url = urljoin(BASE_URL, href)
                url = url.replace(".php", ".html")
                results.append({
                    "url": url,
                    "headline": title,
                    "date": date,
                    "type": TYPE_MAP.get(type_name, "Unknown")
                })
                count += 1
        return results

    def six_rr_plus_parser(html: str):
        soup = BeautifulSoup(html, "html.parser")
        results = []
        for section in soup.select("div.parts_column_02 > div.parts_bg_01"):
            type_heading = section.select_one("section h2.parts_txt_01")
            type_name = type_heading.get_text(strip=True) if type_heading else None
            count = 0
            for a in section.select("ul.archiveNav a[href]"):
                if count >= constants.WANGAN_MAXI_POSTS_PER_SECTION:
                    break
                href = a["href"]
                date_tag = a.find("p")
                title_tag = a.find("h4")
                title = title_tag.get_text(strip=True) if title_tag else "No title"
                date = date_tag.get_text(strip=True) if date_tag else "No date"
                url = urljoin(BASE_URL, href)
                url = url.replace(".php", ".html")
                results.append({
                    "url": url,
                    "headline": title,
                    "date": date,
                    "type": TYPE_MAP.get(type_name, "Unknown")
                })
                count += 1
        return results

    if version == constants.WANGAN_MAXI_VERSION.FIVE_DX_PLUS:
        return five_dx_plus_parser
    elif version == constants.WANGAN_MAXI_VERSION.SIX_RR:
        return six_rr_parser
    elif version == constants.WANGAN_MAXI_VERSION.SIX_RR_PLUS:
        return six_rr_plus_parser


def make_wmmt_news_extractor(identifier: str, version: constants.WANGAN_MAXI_VERSION, region_text: str):
    def five_dx_plus_extractor(html: str, data: dict):
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".parts_inner_01")
        if not container:
            return None
        date_str = data["date"]
        timestamp = int(datetime.strptime(date_str, "%Y/%m/%d").replace(tzinfo=timezone.utc).timestamp())
        content = ""
        paragraphs = container.find_all("p")
        if paragraphs:
            content = paragraphs[0].get_text(" ", strip=True)
            if content and len(content.split()) < 50 and len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    next_p_content = paragraph.get_text(" ", strip=True)
                    content += " " + next_p_content
                    if len(content.split()) >= 50:
                        break
        images = []
        seen_srcs = []
        for img in container.find_all("img"):
            src = img.get("src").replace("./","").lstrip("/")
            if src in seen_srcs:
                continue
            seen_srcs.append(src)
            img_url = fix_image_url_path(data["url"], src)
            parent = img.find_parent("a")
            images.append({
                "image": img_url,
                "link": urljoin(BASE_URL, parent.get("href")) if parent and parent.get("href") else None
            })
        data["type"] = "["+region_text+"]" + " " + data["type"]
        data["identifier"] = identifier
        data["timestamp"] = timestamp
        data["content"] = content
        data["images"] = images
        data["is_ai_summary"] = False
        return data

    def six_rr_extractor(html: str, data: dict):
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".parts_column_02")
        if not container:
            return None
        date_str = data["date"]
        timestamp = int(datetime.strptime(date_str, "%Y/%m/%d").replace(tzinfo=timezone.utc).timestamp())
        paragraphs = container.find_all("p")
        if paragraphs:
            content = paragraphs[0].get_text(" ", strip=True)
            if content and len(content.split()) < 50 and len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    next_p_content = paragraph.get_text(" ", strip=True)
                    content += " " + next_p_content
                    if len(content.split()) >= 50:
                        break
        images = []
        seen_srcs = []
        for img in container.select("img"):
            src = img.get("src").replace("./","").lstrip("/")
            if src in seen_srcs:
                continue
            seen_srcs.append(src)
            img_url = fix_image_url_path(data["url"], src)
            parent = img.find_parent("a")
            images.append({
                "image": img_url,
                "link": urljoin(BASE_URL, parent.get("href")) if parent and parent.get("href") else None
            })
        if data["type"] == "FUTURE LAB":
            images = images[1:]
        data["type"] = "["+region_text+"]" + " " + data["type"]
        data["identifier"] = identifier
        data["timestamp"] = timestamp
        data["content"] = content
        data["images"] = images
        data["is_ai_summary"] = False
        return data

    def six_rr_plus_extractor(html: str, data: dict):
        soup = BeautifulSoup(html, "html.parser")
        container = soup.select_one(".parts_column_02")
        if not container:
            return None
        date_str = data["date"]
        timestamp = int(datetime.strptime(date_str, "%Y/%m/%d").replace(tzinfo=timezone.utc).timestamp())
        paragraphs = container.find_all("p")
        if paragraphs:
            content = paragraphs[0].get_text(" ", strip=True)
            if content and len(content.split()) < 50 and len(paragraphs) > 1:
                for paragraph in paragraphs[1:]:
                    next_p_content = paragraph.get_text(" ", strip=True)
                    content += " " + next_p_content
                    if len(content.split()) >= 50:
                        break
        images = []
        seen_srcs = []
        for img in container.select("img"):
            src = img.get("src").replace("./","").lstrip("/")
            if src in seen_srcs:
                continue
            seen_srcs.append(src)
            img_url = fix_image_url_path(data["url"], src)
            parent = img.find_parent("a")
            images.append({
                "image": img_url,
                "link": urljoin(BASE_URL, parent.get("href")) if parent and parent.get("href") else None
            })
        if data["type"] == "FUTURE LAB":
            images = images[1:]
        data["type"] = "["+region_text+"]" + " " + data["type"]
        data["identifier"] = identifier
        data["timestamp"] = timestamp
        data["content"] = content
        data["images"] = images
        data["is_ai_summary"] = False
        return data

    if version == constants.WANGAN_MAXI_VERSION.FIVE_DX_PLUS:
        return five_dx_plus_extractor
    elif version == constants.WANGAN_MAXI_VERSION.SIX_RR:
        return six_rr_extractor
    elif version == constants.WANGAN_MAXI_VERSION.SIX_RR_PLUS:
        return six_rr_plus_extractor

get_wmmt_na_news_post_links = make_wmmt_parser(constants.WANGAN_MAXI_VERSION.FIVE_DX_PLUS)
get_wmmt_asia_oce_news_post_links = make_wmmt_parser(constants.WANGAN_MAXI_VERSION.SIX_RR)
get_wmmt_jp_news_post_links = make_wmmt_parser(constants.WANGAN_MAXI_VERSION.SIX_RR_PLUS)
parse_wmmt_na_news = make_wmmt_news_extractor("WANGAN_MAXI_NA", constants.WANGAN_MAXI_VERSION.FIVE_DX_PLUS, "NA")
parse_wmmt_asia_oce_news = make_wmmt_news_extractor("WANGAN_MAXI_ASIA_OCE", constants.WANGAN_MAXI_VERSION.SIX_RR, "ASIA/OCE")
parse_wmmt_jp_news = make_wmmt_news_extractor("WANGAN_MAXI_JP", constants.WANGAN_MAXI_VERSION.SIX_RR_PLUS, "JPN")
