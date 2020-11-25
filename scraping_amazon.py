import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
URL = 'https://www.amazon.de/Sony-Vollformat-Digitalkamera-Megapixel-SEL-2870/dp/B00FWUDEEC/ref=sr_1_4?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=sony+a7&qid=1604245969&quartzVehicle=5-672&replacementKeywords=sony&sr=8-4'

def check_price():

	driver = webdriver.Chrome()
	driver.get(URL)

	time.sleep(4)

	soup = BeautifulSoup(driver.page_source,'html5lib')

	title = soup.find('span', class_ = 'a-size-large product-title-word-break').text
	price = soup.find('span', class_ = 'a-size-medium a-color-price priceBlockBuyingPriceString').text

	price = float(price[:-5])

	if (price < 1000):
		send_mail()

	print(title.strip())
	print(price)

	driver.close()