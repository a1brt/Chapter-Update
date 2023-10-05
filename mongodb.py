from pymongo import MongoClient
from os.path import join, dirname
from os import environ
from dotenv import load_dotenv 

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db_name = environ.get("DB_NAME")


client = MongoClient()
db = client.get_database(db_name)
user_collection = db.get_collection("users")
title_collection = db.get_collection("titles")

def get_by_chat_id(chat_id):
    return user_collection.find_one({"chat_id":chat_id})

def get_title_subscribers(title):
    return [id["chat_id"] for id in user_collection.find({"subscribed_to":title})]

def update_user_titles(chat_id, titles):
    user_collection.update_one({"chat_id":chat_id}, {"$set":{"subscribed_to": titles}})

def save_user_info(chat_id):
    user = {
        "chat_id" : chat_id,
        "subscribed_to" :  []
    }
    user_collection.insert_one(user)

def delete_by_chat_id(chat_id):
    user_collection.delete_one({"chat_id": chat_id})

def get_chapters():
    return dict([( t["name"], t["latest_chapter"]) for t in title_collection.find()])

def update_latest_chapter(name:str, chapter:str):
    title_collection.update_one({"name":name}, {"$set":{"latest_chapter": chapter}})
