import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def check_can_send_notifs():
    required_env_vars = [
        "KV_REST_API_URL",
        "KV_REST_API_TOKEN",
        "FIREBASE_SERVICE_ACCOUNT_JSON_PATH"
    ]
    missing_vars = [var for var in required_env_vars if os.environ.get(var) is None]
    if missing_vars:
        return False
    else:
        return True

def get_tokens(topic):
    upstash_rest_api_url = os.environ.get("KV_REST_API_URL")
    upstash_token = os.environ.get("KV_REST_API_TOKEN")
    url = f"{upstash_rest_api_url}/smembers/fcm-{topic}"
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {upstash_token}"}
    )
    if resp.status_code != 200:
        print("Upstash error:", resp.text)
        return []
    data = resp.json()
    return data.get("result", [])

def broadcast_to_topic(topic: str, title: str, body: str, image):
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_JSON_PATH"))
        firebase_admin.initialize_app(cred)

    tokens = get_tokens(topic)
    if not tokens:
        print(f"No tokens found for topic '{topic}'")
        return

    for token in tokens:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image
            ),
            token=token
        )
        try:
            response = messaging.send(message)
            print(f"Sent to {token}: {response}")
        except Exception as e:
            print(f"Error sending to {token}: {e}")

if __name__ == "__main__":
    topic = "sdvx"
    title = "New sdvx Update!"
    body = "Check out the latest DDR content now!"

    broadcast_to_topic(topic, title, body)
