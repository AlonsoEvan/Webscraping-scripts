import re
import json
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time
import random


root_url = 'https://fr.trustpilot.com/review/www.gammvert.fr'
urls = [ '{root}?page={i}'.format(root=root_url, i=i) for i in range(1,3) ]

comms = []
notes = []
dates = []

for url in urls: 
	results = requests.get(url)

	#time.sleep(20)

	soup = BeautifulSoup(results.text, "html.parser")

	commentary = soup.find_all('section', class_='review__content')

	for container in commentary:

		try:
			comm  = container.find('p', class_ = 'review-content__text').text.strip()

		except:
			comm = container.find('a', class_ = 'link link--large link--dark').text.strip()

		comms.append(comm)

		note = container.find('div', class_ = 'star-rating star-rating--medium').find('img')['alt']
		notes.append(note)

		date_tag = container.div.div.find("div", class_="review-content-header__dates")
		date = json.loads(re.search(r"({.*})", str(date_tag)).group(1))["publishedDate"]

		dates.append(date)

data = pd.DataFrame({
	'comms' : comms,
	'notes' : notes,
	'dates' : dates
	})

data['comms'] = data['comms'].str.replace('\n', '')

data['dates'] = pd.to_datetime(data['dates']).dt.date
data['dates'] = pd.to_datetime(data['dates'])


print(data.head())
#data.to_csv('file.csv', sep=';', index=False, encoding = 'utf-8-sig')
