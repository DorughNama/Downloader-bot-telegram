import os

from dotenv import load_dotenv


load_dotenv()


# ======================
# Telegram Bot
# ======================

BOT_TOKEN = os.getenv(
    "BOT_TOKEN"
)


# ======================
# API
# ======================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


API_HOST = "0.0.0.0"

API_PORT = 8000



# ======================
# Force Join
# ======================

CHANNEL_USERNAME = os.getenv(
    "CHANNEL_USERNAME"
)



# ======================
# Developer
# ======================

GITHUB_URL = os.getenv(
    "GITHUB_URL"
)


SUPPORT_USERNAME = os.getenv(
    "SUPPORT_USERNAME"
)



# ======================
# Downloader
# ======================

DOWNLOAD_TIMEOUT = int(
    os.getenv(
        "DOWNLOAD_TIMEOUT",
        300
    )
)



# ======================
# Anti Spam
# ======================

SPAM_DELAY = int(
    os.getenv(
        "SPAM_DELAY",
        15
    )
)