import os
from datetime import datetime
import time
import requests
import openai
import json
from dotenv import load_dotenv
import base64

load_dotenv()

def check_is_generation_possible():
    return os.getenv("OPENAI_API_KEY") is not None and os.getenv("DISCORD_AUTHORIZATION") is not None


def check_is_announcement_image(img_url: str):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    tools = [
        {
            "type": "function",
            "function": {
                "name": "classify_wacca_plus_image",
                "description": "Classify if an image is WACCA PLUS announcement, update, or information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "is_wacca_plus_related": {
                            "type": "boolean",
                            "description": "Is this image related to WACCA PLUS?",
                        },
                        "category": {
                            "type": "string",
                            "enum": ["announcement", "update", "info", "null"],
                            "description": "Category of image if related; otherwise null.",
                        },
                    },
                    "required": ["is_wacca_plus_related", "category"],
                },
            }
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Does this image contain official update, event, or announcement information for the game WACCA PLUS? Ignore unrelated content like gameplay screenshots, score posts, or arcade cabinet photos. Classify accordingly."},
                    {"type": "image_url", "image_url": {"url": img_url}},
                ],
            }
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "classify_wacca_plus_image"}},
    )

    tool_args = response.choices[0].message.tool_calls[0].function.arguments
    parsed_result = json.loads(tool_args)
    return parsed_result["is_wacca_plus_related"], parsed_result["category"]

def _load_cache():
    cache_file = "wac_result_cache.json"
    if not os.path.exists(cache_file):
        with open(cache_file, "w") as file:
            json.dump({}, file)
    with open(cache_file, "r") as file:
        return json.load(file)

def _save_cache(cache: dict):
    cache_file = "wac_result_cache.json"
    with open(cache_file, "w") as file:
        json.dump(cache, file)

def _convert_image_to_base64(img_url: str):
    response = requests.get(img_url)
    if response.status_code == 200:
        img_data = response.content
        img_base64 = base64.b64encode(img_data).decode('utf-8')
        mime_type = response.headers['Content-Type']
        return f"data:{mime_type};base64,{img_base64}"
    else:
        raise Exception(f"Failed to fetch image from URL: {img_url}, status code: {response.status_code}")

def parse_announcement_messages(message_json: dict):
    news_posts = []
    cache = _load_cache()
    for message in message_json:
        type = None
        if len(message["attachments"]) == 0:
            continue
        image_attachments = []
        for attachment in message["attachments"]:
            if "image" in attachment["content_type"]:
                image_attachments.append(attachment)

        if len(image_attachments) == 0:
            continue

        filtered_images = []
        for image in image_attachments:
            if image["id"] in cache:
                is_related = cache[image["id"]][0]
                type = cache[image["id"]][1]
            else:
                is_related, type = check_is_announcement_image(image["url"])
                cache[image["id"]] = [is_related, type]
            if not is_related:
                continue
            filtered_images.append({"image": _convert_image_to_base64(image["url"]), "url": None})

        if len(filtered_images) == 0:
            continue

        date = message["timestamp"].split("T")[0]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        unix_time = int(time.mktime(date_obj.timetuple()))

        news_posts.append({
            "date": date,
            "identifier": "WACCA_PLUS",
            "type": type,
            "timestamp": unix_time,
            "content": "NEW INFORMATION FROM WACCA+ / WACCA+ の最新情報",
            "headline": None,
            "url": None,
            "images": filtered_images
        })

    _save_cache(cache)
    return news_posts
