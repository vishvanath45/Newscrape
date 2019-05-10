"""
This module scrapes content from NEWS18 News.

It provides:
- get_chronological_headlines(url)
- get_trending_headlines(url)
"""

import os
from datetime import datetime
from sys import path

import requests
from bs4 import BeautifulSoup, NavigableString

path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from newscrape_common import (is_string, ist_to_utc, remove_duplicate_entries,
                              str_is_set)
from sources import KNOWN_NEWS_SOURCES



def get_all_content(objects):
    """
    Call this function with a list of objects. Make sure there are no duplicate
    copies of an object else downloading might take long time.
    """
    def get_content(obj):
        from time import sleep
        sleep(0.7)
        response = requests.get(obj["link"])
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            pub_tag = soup.find("span", id="pub_date")
            str_time = pub_tag.find("script").text.split("'")[1].split(
                "<strong>First Published:</strong> "
            )[1]
            obj["published_at"] = ist_to_utc(datetime.strptime(
                str_time,
                "%B %d, %Y, %I:%M %p %Z"
            )).isoformat()
            for i in soup.find("div", id="article_body").find_all("style"):
                i.decompose()
            soup.find("div", id="article_body").find("div", {
                "class": "tag"
            }).decompose()
            obj["content"] = soup.find("div", id="article_body").text
        return "NA"

    for obj in objects:
        get_content(obj)


def get_headline_details(obj):
    try:
        if isinstance(obj.contents[0], NavigableString):
            title = obj.contents[0]
        else:
            title = obj.find("img").get("title")
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": None,
            "title": title
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", {"class": "vodeoiconb"}):
            tag.parent.decompose()
        for tag in soup.find_all("span", {"class": "video_icon_ss"}):
            tag.parent.parent.decompose()
        a_tags = (
            soup.find("div", {"class": "hotTopic"}).find_all("a") +
            soup.find("div", {"class": "blog-list"}).find_all("a")
        )
        headlines = list(map(get_headline_details, a_tags))
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("span", {"class": "video_icon_ss"}):
            tag.parent.parent.decompose()
        a_tags = soup.find("div", id="left").find("div", {
            "class": "flex-box"
        }).find_all("a")
        headlines = remove_duplicate_entries(
            map(get_headline_details, a_tags),
            "link"
        )
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["NEWS18"]

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
