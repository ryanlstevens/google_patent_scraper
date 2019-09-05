# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Example 1: Scrape a single patent 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~ Import packages ~ #
from google_patent_scraper import scraper_class

# ~ Initialize scraper class ~ #
scraper=scraper_class()

# ~~ Scrape patents individually ~~ #
patent_1 = 'US2668287A'
patent_2 = 'US266827A'
err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)
err_2, soup_2, url_2 = scraper.request_single_patent(patent_2)

# ~ Parse results of scrape ~ #
patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)
patent_2_parsed = scraper.get_scraped_data(soup_2,patent_2,url_2)




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# Example 2: Scrape a list of patents 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~ Import packages ~ #
from google_patent_scraper import scraper_class
import json

# ~ Initialize scraper class ~ #
scraper=scraper_class()

# ~ Add patents to list ~ #
scraper.add_patents('US2668287A')
scraper.add_patents('US266827A')

# ~ Scrape all patents ~ #
scraper.scrape_all_patents()

# ~ Get results of scrape ~ #
patent_1_parsed = scraper.parsed_patents['US2668287A']
patent_2_parsed = scraper.parsed_patents['US266827A']

# ~ Print inventors of patent US2668287A ~ #
for inventor in json.loads(patent_1_parsed['inventor_name']):
  print('Patent inventor : {0}'.format(inventor['inventor_name']))