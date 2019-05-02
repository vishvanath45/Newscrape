# Newscrape
Scraping news sources

## Primary Source of news feed

- [ ] Google News
- [x] The Hindu
- [x] Hindustan Times
- [x] Deccan Chronicle
- [ ] Telegraph
- [x] Times of India
- [ ] News18
- [ ] TimesNow
- [x] NDTV 
- [ ] CNN-IBM
- [ ] Yahoo News
- [ ] AajTak
- [ ] Mid Day
- [ ] Rediff 
- [ ] National Herald
- [ ] News Today
- [x] DD News
- [ ] Indian Express
- [ ] PTI


## Using Tools

- [x] Scraping(Beautiful Soup)
- [x] News APIs(requests)
- [ ] Selenium

Initial plan is to look into various feasible ways to extract the headlines from news websites.

## Contributing

### Install requirements
```
pipenv install
```
OR
```
pipenv --three
pipenv shell
pip install -r requirements.txt
```

### Activate virtualenv
```
pipenv shell
```

### Setup mongodb credentials _[optional]_
```
cp .env.example .env
EDITOR=nano $EDITOR .env
```

### Start the main script
If you have setup `mongodb` then you can run the following scripts. Running them will store the scraped content to the database for further analysis.
```
python3 ./update_db_for_archived_news.py
python3 ./update_db_for_trending_news.py
```
If you don't have `mongodb` then just use the following command:
```
python3 ./scraper/dd-news.py
```
Here `dd-news.py` can be replaced with any other news scraper too. This will just give the scraped output and won't store it.

### How to add a new source?

Make sure the name of the python source file is in lowercase and doesn't contain punctuation characters. If the news source name is **News Source** then the corresponding filename should be `news-source.py` and should be kept in `scraper/` directory.

#### Using `BeautifulSoup`
Reusing `the-hindu.py` is the best option to start writing a new parser for a news source.

Also add details of the source in `sources.py`.

### Mandatory functions
You will have to keep a `get_headlines(url)` function in the python module, else running `update_db_for_*_news.py` will throw error. For consistency you can keep `get_headline_details` and `get_all_content` also which are used to find headline details and news content respectively.

## Authors
- [Debasis Mitra](https://www.nitdgp.ac.in/faculty/c8a7fd24-de21-4537-8e67-acab7d45b9d2)
- [vishvanath45](https://github.com/vishvanath45)
- [Compro-Prasad](https://github.com/Compro-Prasad)
