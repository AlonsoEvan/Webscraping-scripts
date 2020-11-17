import pandas as pd

from requests import get
from bs4 import BeautifulSoup

from IPython.core.display import clear_output

from time import sleep
from random import randint
from time import time


names = []
years = []
imdb_ratings = []
metascores = []
votes = []
#gross=[] #many movies have no record
movie_description=[]
movie_duration=[]
movie_genres=[]


headers = {"Accept-Language": "en-US, en;q=0.5"}

pages = [str(i) for i in range(1,4)] #for now we want ton only scrape 5 pages, but if you want more, just change the number
years_url = [str(i) for i in range(2000,2018)]

start_time = time()
requests = 0


#for now we want ton only scrape 5 pages, but if you want more, just change the number
for _ in range(5):
	requests += 1
	sleep(randint(1,3))
	elapsed_time = time() - start_time
	print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))


for year_url in years_url:

	for page in pages:

		response = get('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page, headers = headers)
		sleep(randint(8,15))

		requests += 1
		elapsed_time = time() - start_time
		print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
		clear_output(wait = True)



		soup = BeautifulSoup(response.text, 'html.parser')


		movies_containers = soup.find_all('div', class_ = 'lister-item mode-advanced')




		for container in movies_containers:
			if container.find_all('div', class_ = 'ratings-metascore') is not None:

				name = container.find('h3', class_ = 'lister-item-header').a.text
				names.append(name)

				year = container.h3.find('span', class_ = 'lister-item-year text-muted unbold').text
				year = year.replace('(', ' ')
				year = year.replace(')', ' ')
				years.append(year)

				imdb_rating = float(container.find('div', class_ = 'inline-block ratings-imdb-rating').text)
				imdb_ratings.append(imdb_rating)

				score = container.find('span', class_ = 'metascore')
				if score:
					metascores.append(score.getText(strip = True))
				else:
					metascores.append(None)

				vote = container.find('span', attrs = {'name' : 'nv'}).text
				vote = vote.replace(',', '')
				votes.append(int(vote))

				movie_desc = container.find_all('p', class_ = 'text-muted')[1].text
				movie_desc = movie_desc.replace(',', ' ')
				movie_description.append(movie_desc)


				movie_info = container.find_all('p', class_ = 'text-muted')[0]

				movie_runtime = movie_info.find('span', class_ = 'runtime').text
				movie_duration.append(movie_runtime)

				movie_genre = movie_info.find('span', class_ = 'genre').text
				movie_genre = movie_genre.replace(',', ' ')
				movie_genres.append(movie_genre)



df = pd.DataFrame({'movie': names,
'year': years,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
#'gross':gross,
'movie decription':movie_description,
'movie duration':movie_duration,
'movie genre':movie_genres
})



df.to_csv('finaldf.csv')




