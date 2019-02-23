#!/usr/bin/env python3


def is_string(obj):
    return isinstance(obj, str)


def strip_string(s):
    return s.strip()


def str_is_set(attr):
    return attr and attr != ""


def get_headline_details(obj):
    try:
        return {
            "href": obj["href"],
            "content": "\n".join(filter(
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


def get_headlines(text):
    soup = BeautifulSoup(text, 'html.parser')
    main_div = soup.find("div", {
        "class": "justin-text-cont"
    })
    headline_tags = main_div.find_all("a", href=str_is_set)
    return list(map(get_headline_details, headline_tags))


if __name__ == "__main__":
    import requests
    import json
    from bs4 import BeautifulSoup

    # Don't change this unknowingly
    NEWS_WEBSITE = "https://www.thehindu.com/"

    response = requests.get(NEWS_WEBSITE)

    if (response.status_code == 200):
        print(json.dumps(
            get_headlines(response.text),
            sort_keys=True,
            indent=4)
        )
    else:
        print("Error")
