import os
from urllib.parse import quote

import requests
from dotenv import load_dotenv


ENV_FILE = os.path.join(
    os.path.dirname(__file__),
    ".env",
)

load_dotenv(ENV_FILE)


backend_url = os.getenv(
    "backend_url",
    "http://localhost:3030",
).rstrip("/")


sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url",
    "http://localhost:5050/",
).rstrip("/")


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint

    try:
        response = requests.get(
            request_url,
            params=kwargs or None,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Backend request failed: {error}")
        return []


def analyze_review_sentiments(text):
    encoded_text = quote(text, safe="")

    request_url = (
        sentiment_analyzer_url
        + "/analyze/"
        + encoded_text
    )

    try:
        response = requests.get(
            request_url,
            timeout=10,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as error:
        print(f"Sentiment request failed: {error}")

        return {
            "sentiment": "neutral"
        }


def post_review(data_dict):
    request_url = backend_url + "/insert_review"

    response = requests.post(
        request_url,
        json=data_dict,
        timeout=10,
    )

    response.raise_for_status()

    return response.json()