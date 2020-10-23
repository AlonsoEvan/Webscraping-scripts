import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

results = requests.get(url)

soup = BeautifulSoup(results.text, "html.parser")

titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []


movie_div = soup.find_all('div', class_='lister-item mode-advanced')

for container in movie_div:
	names  = container.h3.a.text
	titles.append(names)

	year  = container.h3.find('span', class_ = "lister-item-year").text
	years.append(year)

	runtime = container.p.find('span', class_ = "runtime").text if container.p.find('span', class_ = "runtime") else ''
	time.append(runtime)

	rating = float(container.strong.text)
	imdb_ratings.append(rating)

	meta = container.find('span', class_ = "metascore").text if container.find('span', class_ = "metascore") else '-'
	metascores.append(meta)

	nv = container.find_all('span', attrs = {'name' : 'nv'})

	vote = nv[0].text 
	votes.append(vote)

	grosses = nv[1].text if len(nv) > 1 else '-'
	us_gross.append(grosses)


movies = pd.DataFrame({
	'movies' : titles,
	'year': years,
	'timeMin' : time,
	'imdb' : imdb_ratings,
	'metascore' : metascores,
	'votes' : votes,
	'us_grossMillions' : us_gross
	})



movies['year'] = movies["year"].str.extract('(\d+)').astype(int) #keep (extract) all the digits in the string

movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)

#movies['metascore'] = movies['metascore'].astype(int)

movies['votes'] = movies['votes'].str.replace(',', '').astype(int)

movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))

movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')



movies.to_csv('df.csv')

print(movies.head())