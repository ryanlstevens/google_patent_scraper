# Patent Scraper
A python package to scrape patents from 'https://patents.google.com/'. The package is made up a single python class, google_scraper(). This scraper can be used both to retreive parsed html of a single patents page or a list of patents.

## Main Use Cases

There are two primary ways to use this package:
1. Scrape a single patent

``` javascript
# ~ Import packages ~ #
from patent_scraper import google_scraper
import json

# ~ Initialize scraper class ~ #
scraper=google_scrape() 

# ~ Scrape patents individually ~ #
#
# Request single patent returns whether the scrape
#  was successful and the parsed html using bs4
err_1, soup_1 = scraper.request_single_patent('US2668287A')
err_2, soup_2 = scraper.request_single_patent('US266827A')

# ~ Parse results of scrape ~ #
patent_1_parsed = scraper.process_patent_html(soup_1)
patent_2_parsed = scraper.process_patent_html(soup_2)
```

2. Scrape a list of patents

```javascript
# ~ Import packages ~ #
from patent_scraper import google_scraper
import json

# ~ Initialize scraper class ~ #
scraper=google_scrape() #<- Initialize class

# ~ Add patents to list ~ #
scraper.add_patents('2668287A')
scraper.add_patents('266827A')

# ~ Scrape all patents ~ #
scraper.scrape_all_patents()

# ~ Get results of scrape ~ #
patent_1_parsed = scraper.parsed_patents['US2668287A']
patent_2_parsed = scraper.parsed_patents['US266827A']

# ~ Print inventors of patent US2668287A ~ #
for inventor in json.loads(patent_1_parsed['inventor_name']):
  print('Patent inventor : {0}'.format(inventor['inventor_name']) 
```


### Example Files

I have provided two seperate example scripts for usage of this package:
  1. Scrape a patent
  2. Scrape many patents using multiprocessing module

