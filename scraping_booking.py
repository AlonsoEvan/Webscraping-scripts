
import pandas as pd

import time
import requests
from bs4 import BeautifulSoup

import re


root_url = 'https://www.booking.com/reviews/fr/hotel/elyseesunion.fr.html?page='
urls = [ '{root}{i};r_lang=fr;rows=75,'.format(root=root_url, i=i) for i in range(1,30,1) ]

#url='https://www.booking.com/reviews/fr/hotel/elyseesunion.fr.html?page=1;r_lang=all;rows=75,'


headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}


commspos = []
commsneg = []
header = []
notes = []
dates = []
datestostay = []


for url in urls: 
    results = requests.get(url, headers = headers)

    #time.sleep(10)

    soup = BeautifulSoup(results.text, "html.parser")

    reviews = soup.find_all('li', class_ = "review_item clearfix")

    for review in reviews:

        try:
            commpos  = review.find("p", class_  = "review_pos").text.strip()
        except:
            commpos = 'NA'

        commspos.append(commpos)


        try:
            commneg  = review.find("p", class_  = "review_neg").text.strip()
        except:
            commneg = 'NA'

        commsneg.append(commneg)


        head = review.find('div', class_ = 'review_item_header_content').text.strip()
        header.append(head)


        note = review.find('span', class_ = 'review-score-badge').text.strip()
        notes.append(note)


        date = review.find('p', class_ = 'review_item_date').text[23:].strip()
        dates.append(date)


        try:
            datestay = review.find('p', class_ = 'review_staydate').text[20:].strip()
            datestostay.append(datestay)
        except:
            datestostay.append('NaN')





data = pd.DataFrame({
    'commspos' : commspos,
    'commsneg' : commsneg,
    'headers' : header,
    'notes' : notes,
    'dates' : dates,
    'datestostay' : datestostay,
    })


data = data[data['datestostay'] != 'NaN']


#pd.to_datetime(my_series, format='%d %b. %Y')


frenc_to_eng = {'janvier': '1', 'février': '2', 'mars': '3', 'avril': '4', 'mai': '5', 'juin': '6', 'juillet': '7', 'août': '8', 'septembre': '9', 'octobre': '10', 'novembre': '11', 'décembre': '12'}
 
# make new columsn for day month and year. FOr month, map the french name to month numbers
data['day'] = data['dates'].apply(lambda x : x.split(' ')[0])
data['month'] = data['dates'].apply(lambda x : x.split(' ')[1]).map(frenc_to_eng)
data['year'] = data['dates'].apply(lambda x : x.split(' ')[2])

# make date time column from year, month and day.
data['date'] = pd.to_datetime(data['year']+'-'+data['month']+'-'+data['day'],format='%Y-%m-%d')
data['date'] = pd.to_datetime(data['date']).dt.date
data['date'] = pd.to_datetime(data['date'])
data['date'] = data.date.dt.strftime('%Y-%m')






data['month2'] = data['datestostay'].apply(lambda x : x.split(' ')[0]).map(frenc_to_eng)
data['year2'] = data['datestostay'].apply(lambda x : x.split(' ')[1])

# make date time column from year, month and day.
data['datetostay'] = pd.to_datetime(data['year2']+'-'+data['month2'],format='%Y-%m')
data['datetostay'] = pd.to_datetime(data['datetostay']).dt.date
data['datetostay'] = pd.to_datetime(data['datetostay'])
data['datetostay'] = data.datetostay.dt.strftime('%Y-%m')

data.drop((['day', 'month', 'year', 'month2', 'year2']), axis = 1, inplace = True)





data_out = []

for s in data['commspos']:

    data_out.append(re.sub(r'[\t\n\r ]+', ' ', str(s)).strip())
    
data['commspos'] = data_out


data_out2 = []

for s in data['commsneg']:

    data_out2.append(re.sub(r'[\t\n\r ]+', ' ', str(s)).strip())
    
data['commsneg'] = data_out2



#print(data['datetostay'].head())

data.to_csv('dftest.csv', sep=';', index=False, encoding = 'utf_8_sig')









#https://strftime.org/

#https://www.booking.com/reviews/co/hotel/ibis-bogota-museo.es.html?page=1;r_lang=all;rows=75,

#https://stackoverflow.com/questions/55669071/scraping-booking-coments-with-python