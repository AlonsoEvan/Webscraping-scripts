from selenium import webdriver
import time

from selenium.webdriver.support.select import Select

from selenium.webdriver.support.ui import WebDriverWait     
from selenium.webdriver.common.by import By     
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#chemin du folder ou vous avez placer votre chromedriver
PATH = "driver\chromedriver.exe"

options = webdriver.ChromeOptions() 
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200,900")
options.add_argument('enable-logging')

driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get('https://www.booking.com/index.fr.html?label=gen173nr-1DCA0oTUIMZWx5c2Vlc3VuaW9uSA1YBGhNiAEBmAENuAEXyAEM2AED6AEB-AECiAIBqAIDuAL_5ZqEBsACAdICJDcxYjgyZmI2LTFlYWQtNGZjOS04Y2U2LTkwNTQyZjI5OWY1YtgCBOACAQ&sid=303509179a2849df63e4d1e5bc1ab1e3&srpvid=e6ae6d1417bd00a1&click_from_logo=1')
driver.maximize_window()
time.sleep(2)



cookie = driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]')
try:
    cookie.click()
except:
    pass

time.sleep(2)



job_title = driver.find_element_by_xpath('//*[@id="ss"]')
job_title.click()
job_title.send_keys('Paris') #ici on renseigne la ville, attention à la syntaxe
time.sleep(3)

search = driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[4]/div[2]/button')
search.click()
time.sleep(3)




linksfinal = []

n = 3 #le nombre de pages que vous voulez parcourir

for x in range(n): #iterate over n pages

    time.sleep(3)

    my_elems = driver.find_elements_by_xpath('//a[@class="js-sr-hotel-link hotel_name_link url"]')

    links = [my_elem.get_attribute("href") for my_elem in my_elems]

    links = [link.replace('\n','') for link in links]

    linksfinal = linksfinal + links

    time.sleep(3) 

    next = driver.find_element_by_xpath('//*[@id="search_results_table"]/div[4]/nav/ul/li[3]/a')
      
    next.click()



pointforts = []
hotels = []
notes = []

for url in linksfinal: 

    results = requests.get(url)
    soup = BeautifulSoup(results.text, "html.parser")

    try:
        div = soup.find("div", {"class": "hp_desc_important_facilities clearfix hp_desc_important_facilities--bui"})
        pointfort = [x['data-name-en'] for x in div.select('div[class*="important_facility"]')]
        pointforts.append(pointfort)
    except:
        pointforts.append('Nan')

    try:    
        note = soup.find('div', class_ = 'bui-review-score__badge').text
        notes.append(note)
    except:
        notes.append('Nan')
    
    try:
        hotel = soup.find("h2",attrs={"id":"hp_hotel_name"}).text.strip("\n").split("\n")[1]
        hotels.append(hotel)
    except:
        hotels.append('Nan')


data = pd.DataFrame({
    'Notes' : notes,
    'Points fort' : pointforts,
    'Nom' : hotels})

data.to_csv('datatest.csv', sep=';', index=False, encoding = 'utf_8_sig')


driver.close()
