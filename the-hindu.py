#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pytz

def is_string(obj):
    return isinstance(obj, str)


def strip_string(s):
    return s.strip()


def str_is_set(attr):
    return attr and attr != ""


def get_content(url):
    import re
    response = requests.get(url)
    if response.status_code == 200:
        html_content = BeautifulSoup(response.text, 'html.parser')
        text = html_content.find("div", {
            "class": "article"
        }).find("div", id=re.compile('content-body*')).get_text()
        return text
    return "NA"


i = 0
def get_headline_details(obj):
    try:
        from datetime import datetime
        from time import sleep
        sleep(1)
        global i
        print("Downloading " + str(i) + " article")
        i += 1
        return {
            "content": get_content(obj["href"]),
            "link": obj["href"],
            "timestamp": str(datetime.now(tz=pytz.timezone('Asia/Kolkata'))),
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


def get_headlines(url):
    response = requests.get(url)
    if (response.status_code == 200):
        soup = BeautifulSoup(response.text, 'html.parser')
        main_div = soup.find("div", {
            "class": "justin-text-cont"
        })
        headline_tags = main_div.find_all("a", href=str_is_set)
        return list(map(get_headline_details, headline_tags))[:10]
    return None


if __name__ == "__main__":
    import json

    # Don't change this unknowingly
    NEWS_WEBSITE = "https://www.thehindu.com/"

    print(json.dumps(
        get_headlines(NEWS_WEBSITE),
        sort_keys=True,
        indent=4
    ))
