import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
URL_AUTH = os.getenv('URL_AUTH')
GET_GROUP = os.getenv('GET_GROUP')
