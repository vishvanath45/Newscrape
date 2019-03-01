#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import itertools

def is_string(obj):
    return isinstance(obj, str)


def strip_string(s):
    return s.strip()


def str_is_set(attr):
    return attr and attr != ""


def get_content(url):
    return "NA"


def get_all_content(objects):
    """
    Call this function with a list of objects. Make sure there are no duplicate
    copies of an objects else downloading might take long time.
    """
    for obj in objects:
        obj["content"] = get_content(obj["link"])


def get_headline_details(obj):
    try:
        from datetime import datetime
        return {
            "content": "NA",
            "link": obj["href"].split("?")[0],
            "timestamp": str(datetime.utcnow()),
            "title": "\n".join(filter(
                str_is_set,
                map(
                    strip_string,
                    filter(is_string, obj.contents)
                )
            ))
        }
    except KeyError:
        import pdb
        pdb.set_trace()


def get_chronological_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        headline_tags = list(map( lambda x : x.find("a"), soup.find_all("div", {
            "class": "new_storylising_contentwrap"
        })))[:10]

        headlines = list(map(get_headline_details, headline_tags))
        get_all_content(headlines)
        return headlines
    return None


def opinion_class_checker(tag):
    if tag.name == "div" and tag.get("class") is not None and "opinion_opt" in tag.get("class"):
        return False
    return True


def get_trending_headlines(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = list(itertools.chain.from_iterable(map(
            lambda x: x.find_all("a"),
            soup.find('div', id='midcontent').find_all(opinion_class_checker)
        )))
        links = set()
        headlines = list(filter(
            # Getting unique headlines only
            lambda x: [x["link"] not in links, links.add(x["link"])][0],
            map(get_headline_details, a_tags)
        ))
        get_all_content(headlines)
        return headlines
    return None


if __name__ == "__main__":
    import json

    # Don't change this unknowingly
    NEWS_WEBSITE = "https://www.ndtv.com/india"

    print(json.dumps(
        get_chronological_headlines(NEWS_WEBSITE),
        sort_keys=True,
        indent=4
    ))

    print(json.dumps(
        get_trending_headlines("https://www.ndtv.com/"),
        sort_keys=True,
        indent=4
    ))
