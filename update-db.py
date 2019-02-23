#!/usr/bin/env python3

from settings import new_connection
from importlib import import_module


KNOWN_NEWS_SOURCES = [
    {
        "channel": "The Hindu",
        "link": "https://www.thehindu.com/",
    },
    {
        "channel": "NDTV",
        "link": "https://www.ndtv.com/india"
    }
]


def update_database(collection, headlines):
    from pymongo import ReplaceOne
    operations = []
    for headline in headlines:
        operations.append(ReplaceOne(
            filter={ "link": headline["link"] },
            replacement=headline,
            upsert=True
        ))
    new_connection(collection).bulk_write(operations)
    print("OK")


if __name__ == "__main__":
    for src in KNOWN_NEWS_SOURCES:
        src["module"] = src["channel"].lower().replace(" ", "-")
        mod = import_module(src["module"])
        headlines = mod.get_headlines(src["link"])
        update_database(src["channel"], headlines)
