from pymongo import MongoClient
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_name = environ.get("DB_NAME")


client = MongoClient()
db = client.get_database(db_name)
collection = db.get_collection("users")

def get_by_chat_id(chat_id):
    return collection.find_one({"chat_id":chat_id})

def get_title_subscribers(title):
    return [id["chat_id"] for id in collection.find({"subscribed_to":title})]

def update_user_titles(chat_id, titles):
    collection.update_one({"chat_id":chat_id}, {"$set":{"subscribed_to": titles}})

def save_user_info(chat_id):
    user = {
        "chat_id" : chat_id,
        "subscribed_to" :  []
    }
    collection.insert_one(user)

def delete_by_chat_id(chat_id):
    collection.delete_one({"chat_id": chat_id})