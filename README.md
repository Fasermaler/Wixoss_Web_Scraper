# WIXOSS Card Web Crawler

### Introduction

This scraper goes through the card list on the [WIXOSS WIKI](http://selector-wixoss.wikia.com/wiki/Category:WIXOSS_Card) to retrieve the full list of cards and their corresponding information. Documentation available as comments within the script file itself.

Uses the BeautifulSoup4 python library.

Special thanks to user [methylDragon](https://github.com/methylDragon) for coding guidance and inspiration.

### Usage Instructions

1. Clone the repo to a location of your choice.
2. Run **full_wixoss_scraper.py**
3. Once the script completes, there will be 3 CSV files created for each corresponding card type:
   - scraped_data_LRIG.csv
   - scraped_data_SIGNI.csv
   - scraped_data_Spells.csv
