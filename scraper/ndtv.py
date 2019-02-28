#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def is_string(obj):
    return isinstance(obj, str)


def strip_string(s):
    return s.strip()


def str_is_set(attr):
    return attr and attr != ""


def get_content(url):
    return "NA"


def get_headline_details(obj):
    try:
        from datetime import datetime
        return {
            "content": get_content(obj["href"]),
            "link": obj["href"],
            "timestamp": str(datetime.utcnow()),
            "title": obj["title"]
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_tags = list(map( lambda x : x.find("a"), soup.find_all("div", {
            "class": "new_storylising_img"
        })))[:10]

        # It returns 15 results, we are taking just 10 results.
        return list(map(get_headline_details, headline_tags))
    return None


def get_trending_headlines(url):
    pass


if __name__ == "__main__":
    import json

    # Don't change this unknowingly
    NEWS_WEBSITE = "https://www.ndtv.com/india"

    print(json.dumps(
        get_chronological_headlines(NEWS_WEBSITE),
        sort_keys=True,
        indent=4
    ))
