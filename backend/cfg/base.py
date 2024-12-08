import os

from flask.cli import load_dotenv


class BaseConfig:
    load_dotenv()
    BOT_TOKEN = os.getenv('BOT_TOKEN')

    BASE_URL = "https://sploitus.com/"
    QUERY_URL = f"{BASE_URL}?query="

cfg = BaseConfig()