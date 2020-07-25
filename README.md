# Patent Scraper
A python package to scrape patents from 'https://patents.google.com/'. The package is made up of a single python class, scraper_class. This scraper can be used both to retreive parsed html of a single patents page or a list of patents.

The following elements are always returned by the scraper class:

    application_number        (str)   : application number
    inventor_name             (json)  : inventors of patent 
    assignee_name_orig        (json)  : original assignees to patent
    assignee_name_current     (json)  : current assignees to patent
    pub_date                  (str)   : publication date
    filing_date               (str)   : filing date
    priority_date             (str)   : priority date
    grant_date                (str)   : grant date
    forward_cites_no_family   (json)  : forward citations that are not family-to-family cites
    forward_cites_yes_family  (json)  : forward citations that are family-to-family cites
    backward_cites_no_family  (json)  : backward citations that are not family-to-family cites
    backward_cites_yes_family (json)  : backward citations that are family-to-family cites
    
 There are optional elements you can have returned, see examples below:
 
    abstract_text             (str)   : text of abstract (if exists)       

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

### Additional optional information

__Return Abstract Information__

Scrape a patent and retrieve abstract information

``` python
# ~ Import packages ~ #
from google_patent_scraper import scraper_class

# ~ Initialize scraper class ~ #
scraper=scraper_class(return_abstract=True)  #<- TURN ON ABSTRACT TEXT  

# ~~ Scrape patents individually ~~ #
patent_1 = 'US7742806'
err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)

# ~ Parse results of scrape ~ #
patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)

# ~ Print abstract text ~ #
print(patent_1_parsed['abstract_text'])
```


### Example Files

I have provided two seperate example scripts for usage of this package in the /example/ folder:
  1. Examples from this readme: readme_example
  2. Scrape multiple patents using Python's multiprocessing package: multiprocess_example

