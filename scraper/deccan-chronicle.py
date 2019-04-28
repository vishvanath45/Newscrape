"""
This module scrapes content from Deccan Chronicle News.

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
        response = requests.get(url)
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, "html.parser")
            # a bit erraneous
            # contents sometimes include unwanted text when they too are defined in p tag
            contents = html_content.find('div', {'id': 'storyBody'}
                        ).find_all(lambda tag: tag.name == 'p' and not tag.img, recursive=False)
            text = ''
            for cont in contents:
                text += cont.get_text() + '\n'
            return text
        return "NA"

    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.find(
            "span", {"class": "SunChDt2"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[0].strip()
            timestamp = datetime.strptime(
                content,
                "%d %b %Y %I:%M %p"
            )
        return {
            "content": "NA",
            "link": "https://www.deccanchronicle.com" + obj["href"],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": obj.find(['h3', 'h2']).contents[0].strip()
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(
                map( lambda x: x.find("div", {"class": "col-sm-8"}).find("a"),
                    soup.find_all("div", {"class": "col-sm-12 SunChNewListing"})
                    )
                )
        headlines = list(map(get_headline_details, a_tags))
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(soup.find('div', {'class': 'col-sm-7 noPadding'}
                        ).find_all('a', {'class': 'col-sm-12 noPadding'})) + \
                list(soup.find('div', {'class': 'col-sm-5 tsSmall'}
                        ).find_all('a'))[:-1]
        headlines = list(map(get_headline_details, a_tags))
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["Deccan Chronicle"]

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
