"""This modules contains internal database configuration"""
import os

mongo_host = os.getenv("MONGO_HOST", "127.0.0.1")
URL_CONNECTION = f"mongodb://{mongo_host}:27017/"
DB_NAME = "News_feed"
COLLECTION_NAME = "feeds"
