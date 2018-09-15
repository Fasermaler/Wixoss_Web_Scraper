# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 01:01:23 2018

@author: Fasermaler
"""


from pprint import pprint

import requests
from bs4 import BeautifulSoup

import csv


url = "http://selector-wixoss.wikia.com/wiki/Category:WIXOSS_Card"

session = requests.session()
user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text

soup = BeautifulSoup(page_source, "lxml")

links_div = soup.find("tr", {"valign": "top"})

a_tags = links_div.find_all("a")
links_list = []
for i in a_tags:
    
    links_list.append(str(i['href']))
    
#url2 = "http://selector-wixoss.wikia.com" + links_list[2]
url = "http://selector-wixoss.wikia.com" + soup.find("div", {"id": "mw-pages"}).find("a")['href']

while True:
    try:

        session = requests.session()
        user_agent_header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        
        page_source = session.get(url, allow_redirects = True, headers = user_agent_header, verify = False).text
        
        soup = BeautifulSoup(page_source, "lxml")
        
        links_div = soup.find("tr", {"valign": "top"})
        
        a_tags = links_div.find_all("a")
        for i in a_tags:
            links_list.append(str(i['href']))
            
        url = "http://selector-wixoss.wikia.com" + soup.find("div", {"id": "mw-pages"}).find("a").find_next_sibling()['href']
        print(url)
    except:
        break



print(links_list)
