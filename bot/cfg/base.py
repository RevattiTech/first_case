import os
from dotenv import load_dotenv


class Base:
    load_dotenv()
    bot_token = os.getenv('BOT_TOKEN')
    url="http://127.0.0.1:8000/api/v1"

cfg = Base()
