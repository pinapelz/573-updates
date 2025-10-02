from datetime import datetime
from dotenv import load_dotenv
from database import Database
import os
import time
import requests
import openai
import json
import base64
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from summarizer import generate_headline_and_content_from_images

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
    database = Database()
    for message in message_json:
        type = None
        message_content = message.get("content", "")
        if len(message["attachments"]) == 0:
            continue
        image_attachments = []
        for attachment in message["attachments"]:
            if "image" in attachment["content_type"]:
                image_attachments.append(attachment)

        if len(image_attachments) == 0:
            continue

        filtered_images = []
        image_urls = [] # save the images before they get encoded
        for image in image_attachments:
            image_urls.append(image["url"])
            entry = database.get_wac_entry(image["id"])
            if entry:
                is_related = entry[0]
                type = entry[1]
            else:
                is_related, type = check_is_announcement_image(image["url"])
                database.add_new_wac_entry(key=image["id"], is_news=is_related, post_type=type)

            if not is_related:
                continue
            filtered_images.append({"image": _convert_image_to_base64(image["url"]), "url": None})

        if len(filtered_images) == 0:
            continue

        date = message["timestamp"].split("T")[0]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        unix_time = int(time.mktime(date_obj.timetuple()))
        headline, content = generate_headline_and_content_from_images(image_urls, "WACCA PLUS", message_content)

        news_posts.append({
            "date": date,
            "identifier": "WACCA_PLUS",
            "type": type.upper(),
            "timestamp": unix_time,
            "content": content,
            "headline": headline,
            "url": None,
            "images": filtered_images,
            'is_ai_summary': True
        })
    database.close()
    return news_posts
