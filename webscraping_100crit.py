import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

url = "https://www.senscritique.com/films/tops/top111"

results = requests.get(url)

soup = BeautifulSoup(results.text, "html.parser")



titles = []
notes = []
synopsys = []
dates = []
reals = []



for container in soup.find_all('div', class_ = 'elto-flexible-column'):

	#obtain title
	title = container.h2.a.text
	titles.append(title)

	#obtain synopsys
	syno = container.find('p', class_ = 'elco-description').text
	synopsys.append(syno)

	#obtain global rating
	note = float(container.div.a.text)
	notes.append(note)


	#obtain date
	date = container.select_one('time')
	date = date.text if date else '-'
	dates.append(date)

	#obtain realisateur
	real = container.select_one('[class^="elco-baseline-a"]')
	real = real.text if real else '-'
	reals.append(real)



df = pd.DataFrame({
	'Movie' : titles,
	'Ratings' : notes,
	'Movie synopsys' : synopsys,
	'Date' : dates,
	'Realisateur' : reals

	})

import datetime

s = "8 March, 2017"
d = datetime.strptime(s, '%d %B, %Y')
print(d.strftime('%Y-%m-%d'))


df.Date=df.Date.apply(lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))

#df['Year'] = df['Year'].str.extract('(\d+)').astype(int)

#df['Date'] = df['Date'].apply(pd.to_datetime)

#print(df.head())

#print(df.dtypes)

#df.to_csv('df.csv')

print(df.head(10))