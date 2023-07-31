import os
import requests
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

def main():
    """Start the script."""

    print("Connecting to Reddit...")
    message, image_url = "message_test", "https://www.themoviedb.org/t/p/w300_and_h450_bestv2/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg"

    print("Data received. Sending webhook...")
    post_message(message, image_url)

def post_message(message, image_url):
    """Sends the formatted message to a Discord server.

    Parameters
    ----------
    message : str
        The formatted message to post.

    image_url : str
        The URL used as the thumbnail.

    """

    payload = {
        "username": "DVDs Release Dates",
        "embeds": [
            {
                "title": "Top Rising Post",
                "color": 102204,
                "description": message,
                "thumbnail": {"url": image_url},
                "footer": {"text": "Powered by Elf Magic™"}
            }
        ]
    }

    with requests.post(WEBHOOK_URL, json=payload) as response:
        print(response.status_code)


if __name__ == "__main__":
    main()