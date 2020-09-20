from __future__ import annotations

import json
from os import environ

import discord
from pymongo import MongoClient

from models.note import Note
from models.waiting_users import WaitingDMUser, WaitingGuildUser
from util.logger import get_logger

logger = get_logger(__name__)
logger.debug("Waiting for DB connection.")

MAX_ALLOWED_NOTES = int(environ["MAX_ALLOWED_NOTES"])

db_host = environ["DB_HOST"]
client = MongoClient(host=db_host)

logger.debug("Connected to DB")

db = client.get_database(str(environ["DB_NAME"]))
waiting_collection = db.get_collection("waiting_to_add_note")
self_collection = db.get_collection("self_collection")


def add_creating_note_user(member: discord.Member, guild: discord.Guild) -> None:
    """ Adds the user to the waiting collection so that we may
    add their note to the guild when they dm it.

    Args:
        member (discord.Member): Invoking user of !note
        guild (discord.Guild): Guild the user invoked the !note command in
    """
    waiting_user = WaitingGuildUser(
        member.id, guild_id=guild.id, guild_name=guild.name)

    waiting_collection.replace_one({
        "user_id": waiting_user.user_id,
    }, waiting_user.to_dict(), upsert=True)


def add_creating_self_note_user(user: discord.User, msg_id: int) -> None:
    """ Adds the user to the waiting collection so that we may
    add their note to the guild when they dm it.

    Args:
        user (discord.User): Invoking user of !note
        msg_id (int): The id of the invoking message in the dm channel
    """
    waiting_user = WaitingDMUser(user_id=user.id, command_message_id=msg_id)

    waiting_collection.replace_one({
        "user_id": waiting_user.user_id,
    }, waiting_user.to_dict(), upsert=True)


def get_creating_note_user(user: discord.User) -> WaitingGuildUser or WaitingDMUser:
    """ Return a users information that is waiting to get their note added

    Args:
        user (discord.User): The waiting user

    Returns:
        Waiting_Guild_User or WaitingDMUser: The waiting users details,
        either adding a dm note or a note attached to a guild
    """

    existing = waiting_collection.find_one({
        "user_id": user.id
    })

    if not existing:
        return None

    waiting_user = None
    if existing["note_type"] == "guild_user":
        waiting_user = WaitingGuildUser(
            existing["user_id"], existing["guild_id"], existing["guild_name"])
    elif existing["note_type"] == "dm_user":
        waiting_user = WaitingDMUser(
            existing["user_id"], existing["command_message_id"])

    return waiting_user


def add_guild_note(note: str, waiting_user: WaitingGuildUser):
    """ Adds the users note to the given guild collection as specified in
    waiting_user

    Args:
        note (str): The note string to add - Ideally conforms to <title> | <content>
        waiting_user (Waiting_Guild_User): The user waiting to have their note added

    """

    waiting_collection.delete_one({
        "user_id": waiting_user.user_id
    })

    guild_coll = db.get_collection(str(waiting_user.guild_id))

    res = guild_coll.find_one({
        "user_id": waiting_user.user_id
    })

    if not res:
        num_notes = 0
    else:
        prev_notes = res["notes"]
        num_notes = len(prev_notes)

    if num_notes >= MAX_ALLOWED_NOTES:
        guild_coll.find_one_and_replace({
            "user_id": waiting_user.user_id
        }, {
            "user_id": waiting_user.user_id,
            "notes": [note]
        }, upsert=True)

        return True
    else:
        guild_coll.find_one_and_update({
            "user_id": waiting_user.user_id
        }, {
            "$addToSet": {"notes": note}
        }, upsert=True)

    return False


def add_self_note(note: str, waiting_user: WaitingDMUser) -> bool:
    """ Adds the users note to the self note collection as specified in
    waiting_user

    Args:
        note (str): The note string to add - Ideally conforms to <title> | <content>
        waiting_user (WaitingDMUser): The user waiting to have their note added

    """
    waiting_collection.delete_one({
        "user_id": waiting_user.user_id
    })

    res = self_collection.find_one({
        "user_id": waiting_user.user_id
    })

    if not res:
        num_notes = 0
    else:
        prev_notes = res["notes"]
        num_notes = len(prev_notes)

    if num_notes >= MAX_ALLOWED_NOTES:
        self_collection.find_one_and_replace({
            "user_id": waiting_user.user_id
        }, {
            "user_id": waiting_user.user_id,
            "notes": [note]
        }, upsert=True)

        return True
    else:
        self_collection.find_one_and_update({
            "user_id": waiting_user.user_id
        }, {
            "$addToSet": {"notes": note}
        }, upsert=True)

    return False


def get_member_notes(member: discord.Member, guild: discord.Guild) -> [Note] or None:
    """ Get a guild members notes. Usually called after !notes is invoked in a guild

    Args:
        member (discord.Member): The member retrieving their notes
        guild (discord.Guild): The guild that the notes are attached to

    Returns:
        [Note or None]: The Notes that the user has saved, loaded into Note's
    """
    try:
        db_coll = db.get_collection(str(guild.id))
    except Exception:
        logger.exception("No guild ID given")
        return

    res = db_coll.find_one({
        "user_id": member.id
    })

    if not res:
        return None
    else:
        notes = [Note(details) for details in res["notes"]]

    return notes


def get_self_notes(user: discord.User) -> [Note] or None:
    """ Get a users notes. Usually called after !notes is invoked in a DM

    Args:
        member (discord.Member): The user retrieving their notes

    Returns:
        [Note or None]: The Notes that the user has saved, loaded into Note's
    """
    res = self_collection.find_one({
        "user_id": user.id
    })

    if not res:
        return None
    else:
        notes = [Note(details) for details in res["notes"]]

    return notes


def delete_from_waiting(user_id: int):
    """ Removes a user from the waiting collection

    Args:
        user_id (int): The user id of the user to remove from the waiting collection
    """
    waiting_collection.delete_one({
        "user_id": user_id
    })


def clear_dm_notes(user_id: int):
    """ Deletes a users DM notes

    Args:
        user_id (int): The id of the user the notes belong to
    """
    self_collection.delete_one({
        "user_id": user_id
    })


def clear_guild_notes(user_id: int, guild_id: int):
    """ Deletes a users guild emotes

    Args:
        user_id (int): The id of the user the notes belong to
        guild_id (int): The id of the guild that the notes are associated with
    """
    guild_coll = db.get_collection(str(guild_id))

    guild_coll.delete_one({
        "user_id": user_id
    })


def get_guild_notes(guild_id: int) -> [Note]:
    """ Get all of the notes attached to the given guild

    Args:
        guild_id (int): The guild if of the guild the notes are being retrieved for

    Returns:
        [Note]: The Notes that were in the guilds collection, loaded into Note's
    """
    try:
        db_coll = db.get_collection(str(guild_id))
    except Exception:
        logger.exception("No guild ID given")
        return

    res = db_coll.find({})

    if not res:
        notes = ["You have no DM notes!"]
    else:
        users = [user for user in res]

    notes = []
    for user in users:
        try:
            for note_details in user["notes"]:
                notes.append(note_details)
        except KeyError:
            continue

    return notes


def run_query(query: str, collection: str) -> [dict]:
    """ Run a mongo find query using a query string

    Args:
        query (str): The query query object as a string
        collection (str): The collection to run the query in

    Raises:
        ValueError: Raised if the query string is not a valid json string

    Returns:
        [dict]: The results of the query
    """
    if collection not in db.list_collection_names():
        return

    coll = db.get_collection(collection)

    try:
        target = json.loads(query)
        logger.debug(f"{target=}")
    except ValueError as e:
        logger.exception("Could not decode %s as JSON", query)
        raise e

    return [doc for doc in coll.find(target)]
