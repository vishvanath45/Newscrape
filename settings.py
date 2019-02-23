#!/usr/bin/env python3

from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv


def new_connection(collection):
    """
    Returns a connection to the mongo collection.
    """
    load_dotenv()
    host = getenv("HOST")
    username = getenv("USERNAME")
    password = getenv("PASSWORD")
    database = getenv("DATABASE")
    client = MongoClient(host, serverSelectionTimeoutMS=6000)
    if client.admin.authenticate(username, password, mechanism='SCRAM-SHA-1'):
        data_base = client[database]
        return data_base[collection]
    return None
