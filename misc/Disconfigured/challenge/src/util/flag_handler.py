from __future__ import annotations

from os import environ
import json

from pymongo import MongoClient

from util.logger import get_logger

logger = get_logger(__name__)

db_host = environ["DB_HOST"]
client = MongoClient(host=db_host)

db = client.get_database(str(environ["DB_NAME"]))
ductf_guild_collection = db.get_collection(str(environ["CHALLENGE_SERVER_ID"]))


def add_flag(flag: str):
    """Insert the flag into the DB under the challenge server collection"""
    # Add flag to Jordan's notes
    ductf_guild_collection.insert_one(
        {"user_id": 177022915747905536, "notes": [f"flag | {flag}"]})

    # Add flag to the bots notes
    ductf_guild_collection.insert_one(
        {"user_id": 738992913652121690, "notes": [f"flag | {flag}"]})


def add_dummy_notes(f: FileHandler):
    dummy_notes = json.load(f)

    for user in dummy_notes["users"]:
        ductf_guild_collection.insert_one({
            "user_id": user["user_id"], "notes": user["notes"]
        })
