"""
This module scrapes content from DD News.

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
        response = requests.get(url)
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, "html.parser")
            contents = html_content.find('div', {'class': 'news_content'})
            if not contents:
                return ""
            contents = contents.find_all('p')#lambda tag: tag.name == 'p' and not tag.img, recursive=False)
            text = contents[0].get_text() + '\n' + contents[1].get_text()
            return text
        return "NA"

    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_chronological_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.find(
            "p", {"class": "archive-date"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[0].strip()
            timestamp = datetime.strptime(
                content,
                "%d-%m-%Y | %I:%M %p"
            )
        return {
            "content": "NA",
            "link": "http://ddnews.gov.in" + obj["href"],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": obj.find("p", {"class": "archive-title"}).get_text().strip()
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_trending_headline_details(obj):
    try:
        from datetime import datetime
        timestamp_tag = obj.find(
            "p", {"class": "date"}
        )
        if timestamp_tag is None:
            timestamp = datetime.now()
        else:
            content = timestamp_tag.contents[0].strip()
            timestamp = datetime.strptime(
                content,
                "%d-%m-%Y | %I:%M %p"
            )
        return {
            "content": "NA",
            "link": "http://ddnews.gov.in" + obj.find("a")["href"],
            "scraped_at": datetime.utcnow().isoformat(),
            "published_at": ist_to_utc(timestamp).isoformat(),
            "title": obj.find("a").contents[0].strip()
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        a_tags = list(
                    soup.find('div', {'class': 'view-content'}
                    ).find_all('a')
                )
        headlines = list(map(get_chronological_headline_details, a_tags))
        get_all_content(headlines)  # Fetch contents separately
        return headlines
    return None


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        li_tags = list(
                        soup.find('div', {'class': 'panel-pane pane-views pane-news national'}
                        ).find('div', {'class': 'item-list'}
                        ).find_all('li')
                    )
        headlines = list(map(get_trending_headline_details, li_tags))
        get_all_content(headlines)
        return headlines
    return None


if __name__ == "__main__":
    import json

    SRC = KNOWN_NEWS_SOURCES["DD News"]

    print(json.dumps(
        get_chronological_headlines(SRC["pages"].format(0)), # it should start with 0
        sort_keys=True,
        indent=4
    ))

    print(json.dumps(
        get_trending_headlines(SRC["home"]),
        sort_keys=True,
        indent=4
    ))
