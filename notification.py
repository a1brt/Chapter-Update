import logging
import requests
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
    subscriber_ids =  get_title_subscribers(title)
    for id in subscriber_ids:
        try:
            response = requests.post(apiURL, json={'chat_id': id, 'text': message})
            logging.info(response.text)
        except Exception as e:
            logging.error(e)