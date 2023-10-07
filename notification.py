import grequests
from mongodb import get_title_subscribers
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = environ.get("BOT_TOKEN")

def notify(title: str, chapter:str):
    apiURL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    message = f'New chapter {chapter} for {title} has dropped!'
    subscriber_ids = get_title_subscribers(title)
    rs = (grequests.post(apiURL, json={'chat_id': id, 'text': message}) for id in subscriber_ids)
    grequests.map(rs)
