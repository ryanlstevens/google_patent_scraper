# Patent Scraper
A python package to scrape patents from 'https://patents.google.com/'. The package is made up of a single python class, scraper_class. This scraper can be used both to retreive parsed html of a single patents page or a list of patents.

## Package Installation
The package is available on PyPi, and can be installed using pip:

```python
pip install google_patent_scraper
```

## Main Use Cases

There are two primary ways to use this package:
1. Scrape a single patent

``` python
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
patent_2_parsed = scraper.get_scraped_data(soup_2,patetn_2,url_2)
```

2. Scrape a list of patents

```python
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
```


### Example Files

I have provided two seperate example scripts for usage of this package in the /example/ folder:
  1. Examples from this readme: readme_example
  2. Scrape multiple patents using Python's multiprocessing package: multiprocess_example

