# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 01:46:55 2018

@author: Fasermaler
"""
# pprint really only for debugging
#from pprint import pprint
# Libraries
import requests
from bs4 import BeautifulSoup
import csv
import time

start_time = time.time()
# Full WIXOSS card list 
# But some manipulation is required since the list only displays 200 cards at one time
url = "http://selector-wixoss.wikia.com/wiki/Category:WIXOSS_Card"

# requests the session
session = requests.session()
user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

# Gets the page source from the session
page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text

# Converts the page source into beautiful beautiful and delicious soup :D
soup = BeautifulSoup(page_source, "lxml")
# Find the div that stores all the links
links_div = soup.find("tr", {"valign": "top"})

#Uncomment to output raw page HTML to file: rawpage.html (useful for debugging)
#with open("rawpage.html", "w", encoding="UTF-8") as file:
#    file.write(str(soup))

# Loads all the links into a list of links (links_list)
a_tags = links_div.find_all("a")
links_list = []
for i in a_tags:
    links_list.append(str(i['href']))

# Because after the first page, the "previous 200" div becomes active, thus we will only loop the process from this point:

url = "http://selector-wixoss.wikia.com" + soup.find("div", {"id": "mw-pages"}).find("a")['href']

while True:
    try:
        # redo the whole loop above except this time the URL has a find_next_sibling
        session = requests.session()
        user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text
        soup = BeautifulSoup(page_source, "lxml")
        links_div = soup.find("tr", {"valign": "top"})
        a_tags = links_div.find_all("a")
        for i in a_tags:
            links_list.append(str(i['href']))
        # Main change compared to above is the following line, we find the next sibling instead to skip the "previous 200" link   
        url = "http://selector-wixoss.wikia.com" + soup.find("div", {"id": "mw-pages"}).find("a").find_next_sibling()['href']
        # Prints URL for debugging
        print(url)
    # The exception is for when the iteration hits the last page and there is no more "next 200" link    
    except:
        break
# Sets up all the CSV headers
with open("scraped_data_Spells.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    writer.writerow(["Name", "Kana", "Romaji", "Color", "Card Type", "Cost", "Limiting Condition", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

with open("scraped_data_LRIG.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    writer.writerow(["Name", "Kana", "Romaji", "Color", "Card Type", "Level", "Limit", "Grow Cost", "LRIG Type", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

with open("scraped_data_SIGNI.csv", "w", newline = "") as f:
    writer = csv.writer(f, delimiter = ",")
    writer.writerow(["Name", "Kana", "Romaji", "Color", "Card Type", "Level", "Power", "Limiting Condition", "Class", "Card Abilities", "Card Abilities(JP)", "Card Abilities(CN)", "Related Cards", "Sets",])

# Gets the total number of cards
total_cards = len(links_list)

# Initializes the variable to count the card numbers
card_number = 0
card_LRIG_number = 0
card_SIGNI_number = 0
card_spells_number = 0
print(str(links_list[1250]))


# Loops the whole process for every link in links_list
for i in range(len(links_list)):
    # Forms the URL
    url = "http://selector-wixoss.wikia.com" + str(links_list[i])

    session = requests.session()
    user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
    page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text
    soup = BeautifulSoup(page_source, "lxml")
    # So because this stupid page exists: http://selector-wixoss.wikia.com/wiki/User_blog:IcyDevil34/Guide_to_Stop_Decks_Examples
    # Like literally the page has nothing
    # We have to check to make sure the page actually has stuff to scrub from now on
    try:
        test = soup.find("div", {"class", "page-header__categories-links"}).find("a").find_next_sibling().find_next_sibling().text
        #Creates List that stores all card data for this specific card
        card_data = []
        #Gets card name and adds it to the card_data list
        card_data.append(soup.find("h1", {"class": "page-header__title"}).text)
        
        #Find ths the info container table
        info_container = soup.find("div", {"id":"info_container"})
        info_tr = info_container.find("div").find("table").find_all("tr")
        
        # Initializes a variable to check the element number
        e = 0
        for i in info_tr:
            tr_iterable = i.find_all("td")
            table_data = [x.text.strip() for x in tr_iterable]
            #print(table_data[1])
            # Checks to make sure that the 3rd element doesn't have Chinese
            # Not trying to be racist or anything but because the WIXOSS is very inconsistent with whether
            # cards have chinese versions  or not, which makes it hard to format the cards nicely in a table
            if e == 2:
                try:
                    teststring = str(table_data)
                    teststring.encode(encoding='utf-8').decode('ascii')
                    card_data.append(str(table_data[1]))
                    #print("encoding check")
                except UnicodeDecodeError:
                    # Encoding error caused by the fact that there is Chinese, so the element won't be added to the table_data list
                    #print("CHINESE DETECTED")
                    break
            else:
                # Append the table_data to the card_data
                card_data.append(str(table_data[1]))
            e += 1
            
        # Get the ability information table
        ability_tr = info_container.find("div").find_next_sibling().find_all("table")
        #print(ability_tr)
        
        # Get the card ability description and append it to the card_data list
        for i in ability_tr:
            tr_iterable = i.find_all("td")
            table_data = [x.text.strip() for x in tr_iterable]
            #print(table_data[0])
            card_data.append(table_data[0])
        
        # Get the Extra information table
        extra_info_tr = info_container.find("div").find_next_sibling().find_next_sibling().find_all("table")
        #print(extra_info_tr)
        for i in extra_info_tr:
            tr_iterable = i.find_all("td")
            table_data = [x.text.strip() for x in tr_iterable]
            #print(table_data[0])
            card_data.append(table_data[0])
        
        # Get WIXOSS card sets information table
        sets_info_tr = info_container.find("div").find_next_sibling().find_next_sibling().find_next_sibling().find_all("table")
        #print(sets_info_tr)
        
        
        for i in sets_info_tr:
            tr_iterable = i.find_all("a")
            table_data = [x.text.strip() for x in tr_iterable]
        # Condenses the sets into one list element to be added to the card_data list (so they take one cell in the CSV)
        condensed_sets_data = ", ".join(str(e) for e in table_data)
        # Appends the sets information to the card_data list
        card_data.append(condensed_sets_data)
        
        #print(card_data)
        
        # Find out the card type (SIGNI / LRIG / Spell)
        card_type = soup.find("div", {"class", "page-header__categories-links"}).find("a").find_next_sibling().find_next_sibling().text
        
        # Checks the card type and write it to the correct CSV file + Also rereads the line into the console for debugging
        if card_type == "LRIG":
            with open("scraped_data_LRIG.csv", "a", encoding="UTF-8", newline = "") as f:
                writer = csv.writer(f, delimiter = ",")
                writer.writerow(card_data)
                card_LRIG_number += 1
    #        with open("scraped_data_LRIG.csv", "r", encoding="UTF-8") as f:
    #            print(f.read())
                
        elif card_type == "SIGNI":
            with open("scraped_data_SIGNI.csv", "a", encoding="UTF-8", newline = "") as f:
                writer = csv.writer(f, delimiter = ",")     
                writer.writerow(card_data)
                card_SIGNI_number += 1
    #        with open("scraped_data_SIGNI.csv", "r", encoding="UTF-8") as f:
    #            print(f.read())
                
        else:
            with open("scraped_data_Spells.csv", "a", encoding="UTF-8", newline = "") as f:
                writer = csv.writer(f, delimiter = ",")   
                writer.writerow(card_data) 
                card_spells_number += 1
    #        with open("scraped_data_Spells.csv", "r", encoding="UTF-8") as f:
    #            print(f.read())
        card_number += 1
        print("Processed Cards: %d / %d" % (card_number, total_cards))
    except:
        card_number += 1
        print("Bad Card Detected: " + str(card_number) + " Link: " + url)
# Gets the elapsed time
end_time = time.time()
elapsed_time = end_time - start_time
# converts the elapsed time to hours, minutes and seconds
minutes, seconds = divmod(elapsed_time, 60)
hours, minutes = divmod(minutes, 60)
# Completion output
print("Done! Total number of cards is: " + str(card_number))
print("Card Breakdown is as follows")
print("LRIG: " + str(card_LRIG_number) + "   SIGNI: " + str(card_SIGNI_number) + "   Spells: " + str(card_spells_number))
print("Total time taken: %d hours, %02d minutes, %02d seconds" % (hours, minutes, seconds))