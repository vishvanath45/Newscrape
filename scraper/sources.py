"""
All news sources used in the project are defined here.
"""

KNOWN_NEWS_SOURCES = {
    "The Hindu": {
        "home": "https://www.thehindu.com/",
        "india": "https://www.thehindu.com/news/national/",
        "page1": "",
        "pages": "https://www.thehindu.com/news/national/?page={}"
    },
    "NDTV": {
        "home": "https://www.ndtv.com/",
        "india": "https://www.ndtv.com/india",
        "page1": "",
        "pages": "https://www.ndtv.com/india/page-{}"
    },
    "Times of India": {
        "home": "https://timesofindia.indiatimes.com/",
        "india": "https://timesofindia.indiatimes.com/india/",
        "page1": "https://timesofindia.indiatimes.com/india/",
        "pages": "https://timesofindia.indiatimes.com/india/{}"
    },
    "Hindustan Times": {
        "home": "https://www.hindustantimes.com/",
        "india": "https://www.hindustantimes.com/india-news/",
        "page1": "",
        "pages": "https://www.hindustantimes.com/latest-news/?pageno={}"
    },
    "Deccan Chronicle": {
        "home": "https://www.deccanchronicle.com/",
        "india": "https://www.deccanchronicle.com/nation",
        "page1": "",
        "pages": "https://www.deccanchronicle.com/most-popular?pg={}"
    },
    "DD News": {
        "home": "http://ddnews.gov.in/",
        "india": "http://ddnews.gov.in/national",
        "page1": "http://ddnews.gov.in/about/news-archive?news_type=6",
        "pages": "http://ddnews.gov.in/about/news-archive?news_type=6&page={}"
    },
}
