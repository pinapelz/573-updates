from dotenv import load_dotenv
import openai
import json
import hashlib
import os

load_dotenv()
MAX_CHAR_CONTENT_CONSIDERATION_LENGTH = 1000

def summarization_is_possible() -> bool:
    return os.getenv("OPENAI_API_KEY")


def _load_cache():
    cache_file = "summarization_cache.json"
    if not os.path.exists(cache_file):
        with open(cache_file, "w") as file:
            json.dump({}, file)
    with open(cache_file, "r") as file:
        return json.load(file)


def _save_cache(cache: dict):
    cache_file = "summarization_cache.json"
    with open(cache_file, "w") as file:
        json.dump(cache, file)


def _make_cache_key(game: str, img_urls: list[str]) -> str:
    normalized_game = game.strip().lower()
    img_data = json.dumps(sorted(img_urls), separators=(",", ":"))
    hash_digest = hashlib.sha256(img_data.encode()).hexdigest()[:12]
    return f"{normalized_game}_{hash_digest}"


def generate_headline_and_content_from_images(img_urls: list[str], game: str, message_content: str=""):
    """
    Uses LLM to generate the headline and content when none provided by source, based on one or more images.
    """
    # Limit message content to 500 characters
    if len(message_content) > MAX_CHAR_CONTENT_CONSIDERATION_LENGTH:
        message_content = message_content[:MAX_CHAR_CONTENT_CONSIDERATION_LENGTH]

    cache = _load_cache()
    cache_key = _make_cache_key(game, img_urls)
    if cache_key in cache:
        cached = cache[cache_key]
        return cached["headline"], cached["content"]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "generate_update_text",
                "description": "Generates a concise English headline and short description for a rhythm game update image and the original message content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "headline": {
                            "type": "string",
                            "description": "A short English headline summarizing the game update.",
                        },
                        "content": {
                            "type": "string",
                            "description": "A brief English description of the new content shown in the image(s).",
                        },
                    },
                    "required": ["headline", "content"],
                },
            },
        }
    ]

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        f"Given one or more update-related images for the arcade game {game} and the original Discord message content (limited to 500 characters): '{message_content}', return a short, professional English headline and a brief, stern and concise description summarizing the content. No need to repeat game name"
                    ),
                },
                *[{"type": "image_url", "image_url": {"url": url}} for url in img_urls],
            ],
        }
    ]

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "generate_update_text"},
        },
    )

    tool_result = response.choices[0].message.tool_calls[0].function.arguments
    parsed_result = json.loads(tool_result)
    headline = parsed_result["headline"]
    content = parsed_result["content"]
    cache[cache_key] = {"headline": headline, "content": content}
    _save_cache(cache)
    return headline, content
