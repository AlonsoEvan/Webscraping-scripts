from bs4 import BeautifulSoup as bs 
import requests

import json


def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
    elif row_data.find("br"):
        return [text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")

def clean_tags(soup):
    for tag in soup.find_all(["sup", "span"]):
        tag.decompose()
        
def get_info_box(url):

    r = requests.get(url)
    soup = bs(r.content)
    info_box = soup.find(class_="infobox vevent")
    info_rows = info_box.find_all("tr")
    
    clean_tags(soup)

    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip=True)
        else:
            header = row.find('th')
            if header:
                content_key = row.find("th").get_text(" ", strip=True)
                content_value = get_content_value(row.find("td"))
                movie_info[content_key] = content_value
            
    return movie_info


r = requests.get("https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films")
soup = bs(r.content)
movies = soup.select(".wikitable.sortable i a")

base_path = "https://en.wikipedia.org/"

movie_info_list = []
for index, movie in enumerate(movies):
    if index % 10 == 0:
        print(index)
    try:
        relative_path = movie['href']
        full_path = base_path + relative_path
        title = movie['title']
        
        movie_info_list.append(get_info_box(full_path))
        
    except Exception as e:
        print(movie.get_text())
        print(e)



def minutes_to_integer(running_time):
    if running_time == "N/A":
        return None
    
    if isinstance(running_time, list):
        return int(running_time[0].split(" ")[0])
    else: # is a string
        return int(running_time.split(" ")[0])

for movie in movie_info_list:
    movie['Running time (int)'] = minutes_to_integer(movie.get('Running time', "N/A"))

import re

amounts = r"thousand|million|billion"
number = r"\d+(,\d{3})*\.*\d*"

word_re = rf"\${number}(-|\sto\s|–)?({number})?\s({amounts})"
value_re = rf"\${number}"

def word_to_value(word):
    value_dict = {"thousand": 1000, "million": 1000000, "billion": 1000000000}
    return value_dict[word]

def parse_word_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    word = re.search(amounts, string, flags=re.I).group().lower()
    word_value = word_to_value(word)
    return value*word_value

def parse_value_syntax(string):
    value_string = re.search(number, string).group()
    value = float(value_string.replace(",", ""))
    return value

'''
money_conversion("$12.2 million") --> 12200000 ## Word syntax
money_conversion("$790,000") --> 790000        ## Value syntax
'''
def money_conversion(money):
    if money == "N/A":
        return None

    if isinstance(money, list):
        money = money[0]
        
    word_syntax = re.search(word_re, money, flags=re.I)
    value_syntax = re.search(value_re, money)

    if word_syntax:
        return parse_word_syntax(word_syntax.group())

    elif value_syntax:
        return parse_value_syntax(value_syntax.group())

    else:
        return None

for movie in movie_info_list:
    movie['Budget (float)'] = money_conversion(movie.get('Budget', "N/A"))
    movie['Box office (float)'] = money_conversion(movie.get('Box office', "N/A"))


from datetime import datetime

dates = [movie.get('Release	 date', 'N/A') for movie in movie_info_list]

def clean_date(date):
	return date.split("(")[0].strip()

def date_conversion(date):
	if isinstance(date, list):
		date = date[0]
	if date == 'N/A':
		return None

	date_str = clean_date(date)

	fmts = ["%B %d, %Y", "%d %b %Y"]

	for fmt in fmts:
		try:
			return datetime.strptime(date_str,fmt)
		except:
			pass
	return None

for movie in movie_info_list:
	movie['Release Date (datetime'] = date_conversion(movie.get('Release_date', 'N/A'))






'''
def save_data(title, data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_data(title):
    with open(title, encoding="utf-8") as f:
        return json.load(f)

save_data("disney_data.json", movie_info_list)
'''

import pickle

def save_data_pickle(name, data):
	with open(name ,'wb') as f:
		pickle.dump(data, f)


def load_date_pickle(name):
	with open(name, 'rb') as handle:
		b = pickle.load(handle)

save_data_pickle('disney_data.pickle', movie_info_list)