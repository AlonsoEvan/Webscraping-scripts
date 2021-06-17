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

from selenium import webdriver
import time

from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.common.by import By     
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys


PATH = "driver\chromedriver.exe"

options = webdriver.ChromeOptions() 
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200,900")
options.add_argument('enable-logging')


driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get('https://www.tripadvisor.ca/')
driver.maximize_window()
time.sleep(2)

cookie = driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]')
try:
	cookie.click()
except:
	pass

time.sleep(2)


country = driver.find_element_by_xpath('//input[@placeholder="Where to?"]')
country.click()
country.send_keys('London') #LOCATION TO SPECIFY
country.send_keys(Keys.ENTER)
time.sleep(3)

sectionhotel = driver.find_element_by_xpath('//a[@data-filter-id="LODGING"]')
sectionhotel.click()



linksfinal = []

n = 1

for x in range(n): #iterate over n pages to get the hotels links

	time.sleep(3)

	my_elems = driver.find_elements_by_xpath('//a[@class="review_count"]')

	links = [my_elem.get_attribute("href") for my_elem in my_elems]


	linksfinal = linksfinal + links

	time.sleep(3) 

	next = driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]')
	  
	next.click()

	time.sleep(3)


#linksfinal = ['https://www.tripadvisor.ca/Hotel_Review-g186338-d672863-Reviews-or5-Park_Plaza_County_Hall_London-London_England.html']

j = 2 #number of pages of comments from each hotels

for url in linksfinal: 

	driver.get(url)
	
	results = requests.get(url)

	comms = []
	notes = []
	dates = []
	


	soup = BeautifulSoup(results.text, "html.parser")

	name = soup.find('h1', class_= '_1mTlpMC3').text.strip()

	commentary = soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')

	for k in range(j): #iterate over n pages

		for container in commentary:

			comm  = container.find('q', class_ = 'IRsGHoPm').text.strip()
			comms.append(comm)


			comm1 = str(container.find("div", class_="nf9vGX55").find('span'))
			rat = re.findall(r'\d+', str(comm1))
			rat1 = (str(rat))[2]
			notes.append(rat1)

			

			datereal = container.find("div", class_= "_2fxQ4TOx").text
			datereal = datereal.replace(container.find("a", class_= "ui_header_link _1r_My98y").text, '').replace(' wrote a review',' ')
			dates.append(datereal)

			time.sleep(3)

		nextpages = driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]')

		urlnext = nextpages.get_attribute("href")

		results2 = requests.get(urlnext)

		driver.get(urlnext)

		time.sleep(3)

		soup = BeautifulSoup(results2.text, "html.parser")

		commentary = soup.find_all('div', class_='_2wrUUKlw _3hFEdNs8')


		
	data = pd.DataFrame({
	'comms' : comms,
	'notes' : notes,
	'dates' : dates
	})


	try:
		data['dates'] = pd.to_datetime(data['dates']).dt.date
		data['dates'] = pd.to_datetime(data['dates'])
		data['dates'] = data.dates.dt.strftime('%Y-%m')
	except:
		pass



	data.to_csv(f"{name}.csv", sep=';', index=False)
	#data.to_csv(f"{name} + datetime.now().strftime("_%Y_%m_%d-%I_%M_%S").csv", sep=';', index=False)

	time.sleep(3)










