
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import re


url = 'https://www.bilansgratuits.fr/'

links1 = []

results = requests.get(url)


soup = BeautifulSoup(results.text, "html.parser")

links1 = [a['href']  for a in soup.find("div", {"class": "container_rss blocSecteursActivites"}).find_all('a', href=True)]

secteur = [a.text for a in soup.find("div", {"class": "container_rss blocSecteursActivites"}).find_all('a', href=True)]

links1.pop()
secteur.pop()


secteurs = []
soussecteurs = []
names = []
rank = []

root_url = 'https://www.bilansgratuits.fr/'
urls1 = [ '{root}{i}'.format(root=root_url, i=i) for i in links1 ]


for url, secteur in zip(urls1, secteur):

    results = requests.get(url)

    #time.sleep(20)

    soup = BeautifulSoup(results.text, "html.parser")

    links = [a['href']  for a in soup.find("div", {"class": "listeEntreprises"}).find_all('a', href=True)]

    soussecteur = [a.text for a in soup.find("div", {"class": "listeEntreprises"}).find_all('a', href=True)]

    root_url = 'https://www.bilansgratuits.fr/'
    urls = [ '{root}{i}'.format(root=root_url, i=i) for i in links ]


    for url, soussecteur in zip(urls, soussecteur):

        results = requests.get(url)

        soup = BeautifulSoup(results.text, "html.parser")

        try:
            entries = soup.find('div', {'class': 'donnees'}).find_all('tr')

            for entry in entries:
                secteurs.append(secteur)

            for entry in entries:
                soussecteurs.append(soussecteur)

            for entry in entries:
                names.append(entry.find('a').text) 

            for entry in entries:
                rank.append(entry.find('td').text)               

        except :

            entries = soup.find('div', {'class': 'listeEntreprises'}).find_all('li')


            for entry in entries:
                secteurs.append(secteur)

            for entry in entries:
                soussecteurs.append(soussecteur)

            for entry in entries:
                res = []
                res.append(entry.find('a').text)

                for i in range(0,len(res)):    
                    rx = re.compile(r'[\n\r\t]')

                    res[i] = [item for item in res[i] if not rx.match(item)]

                    for list in res:
                        names.append(''.join([w for w in list]))


            for entry in entries:
                rank.append('Non classé')              



data = pd.DataFrame({
    'Nom de la companie' : names,
    'Secteur' : secteurs,
    "Sous-Secteur" : soussecteurs,
    "Rankings" : rank
    })


data.to_csv('databasebilangratuit2.csv', sep=';', index=False, encoding = 'utf_8_sig')
