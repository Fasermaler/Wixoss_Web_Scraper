# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 20:49:28 2018

@author: Fasermaler
"""

from pprint import pprint
import requests
from bs4 import BeautifulSoup

import csv






#Immediately writes the Headers for the csv file
with open("scraped_data_Spells.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    
    writer.writerow(["Name", "Kana", "Romaji", "Chinese", "Color", "Card Type", "Cost", "Limiting Condition", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

with open("scraped_data_LRIG.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    
    writer.writerow(["Name", "Kana", "Romaji", "Chinese", "Color", "Card Type", "Level", "Limit", "Grow Cost", "LRIG Type", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

with open("scraped_data_SIGNI.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    
    writer.writerow(["Name", "Kana", "Romaji", "Chinese", "Color", "Card Type", "Level", "Power", "Limiting Condition", "Class", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

url = "http://selector-wixoss.wikia.com/wiki/Code_Eat_Mochi_Ice"

session = requests.session()
user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text

soup = BeautifulSoup(page_source, "lxml")

#Uncomment to output raw page HTML to file: rawpage.html (useful for debugging)
#with open("rawpage.html", "w", encoding="UTF-8") as file:
#    file.write(str(soup))

#Creates List that stores all card data for this specific card
card_data = []
#Gets card name and adds it to the card_data list
card_data.append(soup.find("h1", {"class": "page-header__title"}).text)

#Find ths the info container table
info_container = soup.find("div", {"id":"info_container"})
info_tr = info_container.find("div").find("table").find_all("tr")


for i in info_tr:
    tr_iterable = i.find_all("td")
    table_data = [x.text.strip() for x in tr_iterable]
    #print(table_data[1])
    card_data.append(str(table_data[1]))
    
    
ability_tr = info_container.find("div").find_next_sibling().find_all("table")
#print(ability_tr)

for i in ability_tr:
    tr_iterable = i.find_all("td")
    table_data = [x.text.strip() for x in tr_iterable]
    #print(table_data[0])
    card_data.append(table_data[0])
    
extra_info_tr = info_container.find("div").find_next_sibling().find_next_sibling().find_all("table")
#print(extra_info_tr)
for i in extra_info_tr:
    tr_iterable = i.find_all("td")
    table_data = [x.text.strip() for x in tr_iterable]
    #print(table_data[0])
    card_data.append(table_data[0])

sets_info_tr = info_container.find("div").find_next_sibling().find_next_sibling().find_next_sibling().find_all("table")
#print(sets_info_tr)

for i in sets_info_tr:
    tr_iterable = i.find_all("a")
    table_data = [x.text.strip() for x in tr_iterable]
condensed_sets_data = ", ".join(str(e) for e in table_data)
card_data.append(condensed_sets_data)

#print(card_data)
card_type = soup.find("div", {"class", "page-header__categories-links"}).find("a").find_next_sibling().find_next_sibling().text
print(card_type)

if card_type == "LRIG":
    with open("scraped_data_LRIG.csv", "a", encoding="UTF-8", newline = "") as f:
        writer = csv.writer(f, delimiter = ",")
            
        writer.writerow(card_data)
    
    
    with open("scraped_data_LRIG.csv", "r", encoding="UTF-8") as f:
        print(f.read())
elif card_type == "SIGNI":
    with open("scraped_data_SIGNI.csv", "a", encoding="UTF-8", newline = "") as f:
        writer = csv.writer(f, delimiter = ",")
            
        writer.writerow(card_data)
    
    
    with open("scraped_data_SIGNI.csv", "r", encoding="UTF-8") as f:
        print(f.read())
else:
    with open("scraped_data_Spells.csv", "a", encoding="UTF-8", newline = "") as f:
        writer = csv.writer(f, delimiter = ",")
            
        writer.writerow(card_data)
    
    
    with open("scraped_data_Spells.csv", "r", encoding="UTF-8") as f:
        print(f.read())