"""
This module scrapes content from NDTV News.

It provides:
- get_chronological_headlines(url)
- get_trending_headlines(url)
"""

import requests
from bs4 import BeautifulSoup
from sys import path
import os
path.insert(0, os.path.dirname(os.path.realpath(__file__)))
from sources import KNOWN_NEWS_SOURCES
from newscrape_common import   \
    str_is_set, is_string, remove_duplicate_entries, ist_to_utc


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
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "timestamp": ist_to_utc(datetime.utcnow()).isoformat(),
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
                "class": "new_storylising_contentwrap"
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
        soup.find("div", { "class": "opinion_opt" }).decompose()
        # Some anchor tags in div[class="lhs_col_two"] are not parsed by the following
        a_tags = soup.find("div", id="midcontent").find_all(
            "a", { "class": "item-title" }
        )
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link"
        )
        get_all_content(headlines)
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["NDTV"]

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
