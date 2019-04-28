"""
This module scrapes content from Hindustan Times News.

It provides:
- get_chronological_headlines(url)
- get_trending_headlines(url)
"""

import os
from sys import path

import requests
from bs4 import BeautifulSoup

from newscrape_common import (is_string, ist_to_utc, remove_duplicate_entries,
                              str_is_set)
from sources import KNOWN_NEWS_SOURCES

path.insert(0, os.path.dirname(os.path.realpath(__file__)))


def get_all_content(objects):
    """
    Call this function with a list of objects. Make sure there are no duplicate
    copies of an object else downloading might take long time.
    """
    def get_content(url):
        return "NA"

    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.parent.parent.find(
            "span", {"class": "time-dt"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[0].strip()
            timestamp = datetime.strptime(
                content,
                "%b %d, %Y %H:%M"
            )
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": "\n".join(filter(
                str_is_set,
                map(
                    str.strip,
                    filter(is_string, obj.children)
                )
            ))
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(map(
            lambda x: x.find("a"),
            soup.find_all("div", {
                "class": "media-body"
            })
        ))
        headlines = list(map(get_headline_details, a_tags))
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.find("div", { "class": "latestnews-left" }).decompose()
        soup.find("div", { "class": "advertisement-250" }).decompose()
        # to remove sponsered content
        # not sure if tag works every time
        soup.find("div", { "class": "top-thumb mt-20"}).decompose()  
        a_tags = soup.find("div", { 
            "class": "news-area newtop-block mb-5 mt-10" }).find_all(
            "a")
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link",
            "title"
        )
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["Hindustan Times"]

    print(json.dumps(
        get_chronological_headlines(SRC["pages"].format(1)),
        sort_keys=True,
        indent=4
    ))

    print(json.dumps(
        get_trending_headlines(SRC["home"]),
        sort_keys=True,
        indent=4
    ))
