#!/usr/bin/env python3

from scraper.settings import new_connection
from importlib import import_module
from scraper.sources import KNOWN_NEWS_SOURCES

def update_database(collection, headlines):
    if headlines is None:
        return
    from pymongo import InsertOne, UpdateOne
    operations = []
    conn = new_connection(collection + " trending")
    for headline in headlines:
        db_object = {
            "link": headline["link"],
            "start_time": headline["scraped_at"],
            "end_time" : headline["scraped_at"]
        }
        if conn.count_documents({"link": headline["link"]}) > 0:
            operations.append(UpdateOne(
                {"link": headline["link"]},
                {
                    "$set": {"end_time": headline["scraped_at"]}
                }
            ))
        else:
            operations.append(InsertOne(db_object))
    conn.bulk_write(operations)


if __name__ == "__main__":
    for key in KNOWN_NEWS_SOURCES:
        src = KNOWN_NEWS_SOURCES[key]
        src["module"] = "scraper." + key.lower().replace(" ", "-")
        mod = import_module(src["module"])
        try:
            headlines = mod.get_trending_headlines(src["home"])
            update_database(key, headlines)
            print("Done", key)
        except:
            print("ERROR in", key)
