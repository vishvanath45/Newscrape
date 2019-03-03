#!/usr/bin/env python3

from scraper.settings import new_connection
from importlib import import_module
from scraper.sources import KNOWN_NEWS_SOURCES


def update_database(collection, headlines):
    from pymongo import InsertOne
    operations = []
    for headline in headlines:
        operations.append(InsertOne(headline))
    new_connection(collection).bulk_write(operations)
    print("OK")


if __name__ == "__main__":
    for key in KNOWN_NEWS_SOURCES:
        src = KNOWN_NEWS_SOURCES[key]
        src["module"] = "scraper." + key.lower().replace(" ", "-")
        mod = import_module(src["module"])
        headlines = mod.get_chronological_headlines(src["pages"].format(1))
        update_database(key, headlines)
