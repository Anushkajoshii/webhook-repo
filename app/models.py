"""
Database helper functions for MongoDB operations.
"""

from datetime import datetime, timedelta
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def save_event(event_data: dict) -> None:
    """
    Save a webhook event into MongoDB.
    """
    collection.insert_one(event_data)


def get_recent_events(seconds: int = 15) -> list:
    """
    Fetch events created in the last `seconds` window.
    Prevents re-displaying old data.
    """
    time_threshold = datetime.utcnow() - timedelta(seconds=seconds)

    return list(
        collection.find(
            {"created_at": {"$gte": time_threshold}},
            {"_id": 0}
        ).sort("created_at", -1)
    )