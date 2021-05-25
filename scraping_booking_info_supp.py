import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.espncricinfo.com/',
    'Upgrade-Insecure-Requests': '1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

url0 = 'https://www.booking.com/searchresults.fr.html?label=gen173nr-1DCA0oTUIMZWx5c2Vlc3VuaW9uSA1YBGhNiAEBmAENuAEXyAEM2AED6AEB-AECiAIBqAIDuAL_5ZqEBsACAdICJDcxYjgyZmI2LTFlYWQtNGZjOS04Y2U2LTkwNTQyZjI5OWY1YtgCBOACAQ;sid=303509179a2849df63e4d1e5bc1ab1e3;dest_id=-1456928;dest_type=city&'

results = requests.get(url0, headers = headers)
soup = BeautifulSoup(results.text, "html.parser")

links1 = [a['href'].replace('\n','')  for a in soup.find("div", {"class": "hotellist sr_double_search"}).find_all('a', class_ = 'js-sr-hotel-link hotel_name_link url',  href=True)]
root_url = 'https://www.booking.com'
urls1 = [f'{root_url}{i}' for i in links1]

pointforts = []
hotels = []
notes = []

for url in urls1: 
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

#print(data.head(20))
data.to_csv('datatest.csv', sep=';', index=False, encoding = 'utf_8_sig')



#https://stackoverflow.com/questions/67586627/webscraping-script-for-booking-com-doesnt-work/67609518#67609518