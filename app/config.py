"""
Configuration file for MongoDB connection.
"""

import os

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017/"
)

DB_NAME = "github_webhooks"
COLLECTION_NAME = "events"
