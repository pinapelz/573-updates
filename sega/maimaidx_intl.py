from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import json


def parse_maimaidx_intl_api_route(raw_api_data: str, identifier: str, limit: int):
    route_data = json.loads(raw_api_data)
    route_data = route_data[:limit]
    entries = []
    for post_data in route_data:
        date_data = [str(x) for x in post_data["date"]]
        date_str = ".".join(date_data[:3]) # YYYY.MM.DD
        if len(date_data) == 4:
            image_route = f"{date_data[0]}-{date_data[1].zfill(2)}-{date_data[2].zfill(2)}-{date_data[3]}"
        else:
            image_route = f"{date_data[0]}-{date_data[1].zfill(2)}-{date_data[2].zfill(2)}"
        dt = datetime.strptime(date_str, "%Y.%m.%d").replace(tzinfo=timezone(timedelta(hours=9)))
        timestamp = int(dt.timestamp())
        full_image_url = f"https://maimai.sega.com/assets/img/download/pop/download/{image_route}/{post_data['thumb']}"
        if len(date_data) == 4:
            full_image_url = f"https://maimai.sega.com/assets/img/download/pop/download/{image_route}/{post_data['thumb']}"
        content = post_data["desc"] + f"\n\nNew maimai DX International News / maimai DX International の新しいお知らせ\n\n{full_image_url}"
        headline = post_data["title"]
        images = [{
            "image": full_image_url,
            "link": None
        }]
        entry = {
            "date": date_str,
            "identifier": identifier,
            "type": None,
            "timestamp": timestamp,
            "headline": headline,
            "content": content,
            "url": None,
            "images": images,
            "is_ai_summary": False
        }
        entries.append(entry)
    return entries
