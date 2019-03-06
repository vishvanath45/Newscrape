"""
This module scrapes content from The Hindu News.

It provides:
- get_chronological_headlines(url)
- get_trending_headlines(url)
"""

import requests
import re
from datetime import datetime
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
        from time import sleep
        sleep(1)
        response = requests.get(url)
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, "html.parser")
            text = html_content.find("div", {
                "class": "article"
            }).find("div", id=re.compile("content-body*")).get_text()
            return text
        return "NA"

    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_headline_details(obj):
    try:
        timestamp = datetime.strptime(
            obj["title"].split("Published: ")[1].split(" IST")[0],
            "%B %d, %Y %H:%M"
        )
        return {
            "content": "NA",
            "link": obj["href"],
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
        for tag in soup.find_all("div", { "class": "search-scrollar" }):
            tag.decompose()
        main_div = soup.find("section", id="section_2").find(
            "div", { "class": "main" }
        )
        a_tags = list(map(
            lambda x: x.find("a", href=str_is_set),
            main_div.find_all("h3")
        ))
        headlines = list(map(get_headline_details, a_tags))
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def find_a_tag_in_trending(tag):
    if tag.name == "a" and tag.get("title"):
        if re.compile("^Updated: .+Published: .+$").match(tag.get("title")):
            return True
    return False


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        soup.find("div", { "class": "100_3x_JustIn" }).decompose()
        a_tags = soup.find("div", { "class": "main" }).find_all(find_a_tag_in_trending)
        headlines = list(map(get_headline_details, a_tags))
        get_all_content(headlines)
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["The Hindu"]

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
