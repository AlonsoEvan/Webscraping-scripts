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


root_url = 'https://www.tripadvisor.ca/Hotel_Review-g186338-d215539-Reviews-or'
urls = [ '{root}{i}-OYO_Apollo_Hotel_Bayswater-London_England.html#REVIEWS'.format(root=root_url, i=i) for i in range(5,440,5) ]

comms = []
notes = []
#datestostay = []
dates = []


for url in urls: 
	results = requests.get(url)

	 #time.sleep(20)

	soup = BeautifulSoup(results.text, "html.parser")

	commentary = soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')

	for container in commentary:

		comm  = container.find('q', class_ = 'IRsGHoPm').text.strip()
		comms.append(comm)


		#date_tag = container.find("div", class_="_1O8E5N17").text 
		#date_text,date_value = str.split(date_tag,':')
		#datestostay.append(date_value)


		comm1 = str(container.find("div", class_="nf9vGX55").find('span'))
		rat = re.findall(r'\d+', str(comm1))
		rat1 = (str(rat))[2]
		notes.append(rat1)


		datereal = container.find("div", class_= "_2fxQ4TOx").text
		date = datereal[-9:]

		dates.append(date)




data = pd.DataFrame({
	'comms' : comms,
	#'datestostay' : datestostay,
	'notes' : notes,
	'dates' : dates
	})


data['dates'] = pd.to_datetime(data['dates']).dt.date
data['dates'] = pd.to_datetime(data['dates'])
data['dates'] = data.dates.dt.strftime('%Y-%m')

'''
data['datestostay'] = pd.to_datetime(data['datestostay']).dt.date
data['datestostay'] = pd.to_datetime(data['datestostay'])
data['datestostay'] = data.datestostay.dt.strftime('%Y-%m')
'''
#print(data.head())
data.to_csv('table4.csv', sep=';', index=False)