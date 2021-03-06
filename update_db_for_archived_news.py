#!/usr/bin/env python3

from scraper.settings import new_connection
from importlib import import_module
from scraper.sources import KNOWN_NEWS_SOURCES


def update_database(collection, headlines):
    if headlines is None:
        return
    from pymongo import ReplaceOne
    operations = []
    for headline in headlines:
        db_object = {
            "link": headline["link"],
            "published_time": headline["published_at"],
            "content": headline["content"],
            "title": headline["title"]
        }
        operations.append(ReplaceOne(
            filter={ "link": headline["link"] },
            replacement=db_object,
            upsert=True
        ))
    new_connection(collection).bulk_write(operations)


def to_go_on_next_page_or_not(collection, headlines):
    conn = new_connection(collection)
    for x in headlines[:-1]:
        if conn.count_documents({"link": x["link"]}) == 0:
            return True
    return False


if __name__ == "__main__":
    for key in KNOWN_NEWS_SOURCES:
        src = KNOWN_NEWS_SOURCES[key]
        src["module"] = "scraper." + key.lower().replace(" ", "-")
        src["module"] = import_module(src["module"])
    for key in KNOWN_NEWS_SOURCES:
        src = KNOWN_NEWS_SOURCES[key]
        mod = src["module"]
        for i in range(1, 5):
            print(end=".")
            import sys
            sys.stdout.flush()
            try:
                if i == 1 and src["page1"] != "":
                    headlines = mod.get_chronological_headlines(src["page1"])
                else:
                    headlines = mod.get_chronological_headlines(src["pages"].format(i))
                if to_go_on_next_page_or_not(key, headlines):
                    update_database(key, headlines)
                else:
                    break
                print(" " + key + ": Scraping finished till", i - 1)
            except Exception as e:
                print("ERROR in", key)
                break
