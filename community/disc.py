import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_messages(channel_id: str):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages?limit=50"
    headers = {
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB",
        "authorization": os.getenv("DISCORD_AUTHORIZATION"),  # Replace with your real token
        "priority": "u=1, i",
        "sec-ch-ua": '"Not:A-Brand";v="24", "Chromium";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "America/Vancouver",
    }
    response = requests.get(url, headers=headers)
    return response.json()
