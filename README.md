# Scripts to scrape websites

Web scraping is the process of extracting and parsing raw data from the web. Web scraping is a technique which helps data scientist to make their data-rich and is an efficient technique of data collection.

This world is full of data, but unfortunately, most of them are not in the form to be used.

Here's some scripts who aim to scrape some websites. This kind of work is really useful in term of data science value. There is no better way to obtain huge database.

Here's some examples :

## Basic scraping with IMDB (webscraping_imdb)

Here it's a simple script to obtain basic data on IMDB, it's a training script, to familiarize myself with scraping and BeautifulSoup


## Basic scraping with senscritique (webscraping_100crit)

Again, a training script to discover BeautifulSoup


## More complex scraping with Formatic (webscraping_link_formatic)

Here's thing get more complex, it's a script to obtain all the link for the formation in the site. 
The structure was specific hence tough. The page are loaded dynamically with AJAX and need some specification if you want to obtain all the link in all the pages.

The script will return the "formation_link.txt". I put him in the github repository.

## More complex scraping with tripadvisor (webscraping_tripadvisor)

Surely this script could be simplified, I will try to update him as soon as possible.

The script will return the "trip_advisor_database.csv". I put him in the github repository.

## More complex scraping with wikipedia (scraping_wiki2)

This script aims to return data of all the link referenced in animation movie. Like productor, budget, cast and so on. 

The script will return the "data_wiki2.json". I put him in the github repository.

## Basic scraping with scrapy (scrapy_spider)

This script aim to familiarize myself with Scrapy.


## Future Development

- Develop more complexe Scrapy scripts

- Try and familiarize myself with Selenium

- Became very efficient with BeautifSoup.
