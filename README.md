# Newscrape
Scraping news sources

## Primary Source of news feed

- Google News
- The Hindu
- Hindustan Times
- Deccan Chronicle
- Telegraph
- Times of India
- News18
- TimesNow
- NDTV 
- CNN-IBM
- Yahoo News
- AajTak
- Mid Day
- Rediff 
- National Herald
- News Today
- DD News
- Indian Express
- PTI


## Using Tools

- Scraping(Beautiful Soup)
- News APIs
- Selenium

Initial plan is to look into various feasible ways to extract the headlines from news websites.

## Contributing

### Install requirements
```
pipenv install
# OR
pipenv --three # Creates virtualenv
pipenv shell   # Activate virtualenv
pip install -r requirements.txt
```

### Activate virtualenv
```
pipenv shell
```

### Setup mongodb credentials
```
cp .env.example .env
EDITOR=nano $EDITOR .env
```

### Start the main script
```
python3 update-db.py
```

### How to add a new source?

Make sure the name of the python source file is in lowercase and doesn't contain punctuation characters. If the news source name is **News Source** then the corresponding filename should be `news-source.py` and should be kept in project root.

#### Using `BeautifulSoup`
Reusing `the-hindu.py` is the best option to start writing a new parser for a news source.

Also add details of the source in `sources.py`.

### Mandatory functions
You will have to keep a `get_headlines(url)` function in the python module else running `update-db.py` will throw error. For consistency you can keep `get_headline_details` and `get_content` also which are used to find headline details and news content respectively.

## Authors
- [Debasis Mitra](https://www.nitdgp.ac.in/faculty/c8a7fd24-de21-4537-8e67-acab7d45b9d2)
- [vishvanath45](https://github.com/vishvanath45)
- [Compro-Prasad](https://github.com/Compro-Prasad)
