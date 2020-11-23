import pandas as pd
import numpy as np

import selenium
import selenium.webdriver
import time
import random
import os
from bs4 import BeautifulSoup


#get the links

pages = np.arange(1,3)

urls = []

for page in pages:
	page = 'https://www.hostelworld.com/s?q=Barcelona,%20Catalonia,%20Spain&country=Spain&city=Barcelona&type=city&id=83&from=2020-07-03&to=2020-07-05&guests=1&page=' + str(page)

	driver = selenium.webdriver.Chrome()

	driver.get(page)

	time.sleep(random.randint(5,15))

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	urls = [item.get('href') for item in soup.find_all('a')]




#Remove duplicates and none values

urls_final = list(dict.fromkeys(urls))
urls_final = list(filter(None, urls_final))


#Remove if not starting with pwa, remove if ending with display=reviews

urls_final = [x for x in urls_final if x.startswith('/pwa/')]
urls_final = [x for x in urls_final if not x.endswith('display=reviews')]

string = 'https://www.hostelworld.com'

final_list = [string + s for s in urls_final]




#Now that we're having all of our links, let's go scrape the real data



#I will only do it for the first 3 hostels here.
#You could easily change that by modyfing the range.

data = []


driver = selenium.webdriver.Chrome()

for url in final_list[0:3]:
    data.append({})
    filename = ''.join([s if s.isalnum() else '_' for s in url])
    if not os.path.isfile(filename):
        driver.get(url)  
        time.sleep(random.randint(10, 20))
        source = driver.page_source
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(source)
    else:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    soup = BeautifulSoup(source, 'html.parser')

    
    review = soup.find_all(class_='reviews')[-1]
    
    try:
        price = soup.find_all('span', attrs={'class':'price'})[-1] 
    except:
        price = soup.find_all('span', attrs={'class':'price'})

    data[-1]['name'] = soup.find_all(class_=['title-2'])[0].text.strip()
    
    rating_labels = soup.find_all(class_=['rating-label body-3'])
    rating_scores = soup.find_all(class_=['rating-score body-3'])
    assert len(rating_labels) == len(rating_scores)
    for label, score in zip(rating_labels, rating_scores):
        data[-1][label.text.strip()] = score.text.strip()
    
    data[-1]['price'] = price.text.strip()
    data[-1]['number_reviews'] = review.text.strip()  



import pandas as pd
data = pd.DataFrame(data)

#Remove non-string from 2 columns

data['number_reviews'] = data['number_reviews'].str.extract('(\d+)', expand=False)
data['price'] = data['price'].str.extract('(\d+)', expand = False)



df = pd.DataFrame(data)

#print(data.head(10))




