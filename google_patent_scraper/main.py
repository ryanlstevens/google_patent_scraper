# Scrape #
from urllib.request import Request, urlopen
import urllib.parse
from urllib.error import HTTPError 
from bs4 import BeautifulSoup
# json # 
import json
# errors #
from .errors import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#           Create scraper class
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class scraper_class:
    """
    Google scraper class used to scrape data from 'https://patents.google.com/'

    There are two primary ways to use the class:

        (1) Add list of patents to class and scrape all patents at once

        scraper=scraper_class() #<- Initialize class

        # ~ Add patents to list ~ #
        scraper.add_patents('US2668287A')
        scraper.add_patents('US266827A')

        # ~ Scrape all patents ~ #
        scraper.scrape_all_patents()

        # ~ Get results of scrape ~ #
        patent_1_parsed = scraper.parsed_patents['2668287A']
        patent_2_parsed = scraper.parsed_patents['266827A']



        (2) Scrape each patent individually

        scraper=scraper_class() #<- Initialize class

        # ~~ Scrape patents individually ~~ #
        patent_1 = 'US2668287A'
        patent_2 = 'US266827A'
        err_1, soup_1, url_1 = scraper.request_single_patent(patent_1)
        err_2, soup_2, url_2 = scraper.request_single_patent(patent_2)

        # ~ Parse results of scrape ~ #
        patent_1_parsed = scraper.get_scraped_data(soup_1,patent_1,url_1)
        patent_2_parsed = scraper.get_scraped_data(soup_2,patetn_2,url_2)

    Attributes:
        - list_of_patents (list) : patents to be scraped
        - scrape_status   (dict) : status of request using patent
        - parsed_patents  (dict) : result of parsing patent html
        - return_abstract (bool) : boolean for whether the code should return the abstract  

    """
    def __init__(self,return_abstract=False):
        self.list_of_patents = []
        self.scrape_status = {}
        self.parsed_patents = {}
        self.return_abstract = return_abstract

    def add_patents(self, patent):
        """Append patent to patent list attribute self.list_of_patents


        Inputs:
            - patent (str) : patent number 

        """
        # ~ Check if patent is string ~ #
        if not isinstance(patent,str):
            raise(PatentClassError("'patent' variable must be a string"))
        # ~ Append patent to list to be scrapped ~ #
        else:
            self.list_of_patents.append(patent)

    def delete_patents(self,patent):
        """Remove patent from patent list attribute self.list_of_patents

        Inputs:
            - patent (str) : patent number
        """
        # ~ Check if patent is in list ~ #
        if patent in self.list_of_patents:
            self.list_of_patents.pop(self.list_of_patents.index(patent))
        else:
            print('Patent {0} not in patent list'.format(patent))            


    def add_scrape_status(self,patent,success_value):
        """Add status of scrape to dictionary self.scrape_status"""
        self.scrape_status[patent] = success_value

    def request_single_patent(self,patent,url=False):
        """Calls request function to retreive google patent data and parses returned html using BeautifulSoup


        Returns: 
            - Status of scrape   <- String
            - Html of patent     <- BS4 object

        Inputs:
            - patent (str)  : if    url == False then patent is patent number
                              elif  url == True  then patent is google patent url
            - url    (bool) : determines whether patent is treated as patent number 
                                or google patent url

        """
        try:
            if not url:
                url='https://patents.google.com/patent/{0}'.format(patent)
            else:
                url=patent
            print(url)
            req = Request(url,headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, features="lxml")
            return(('Success',soup,url))
        except HTTPError as e:
            print('Patent: {0}, Error Status Code : {1}'.format(patent,e.code))
            return(e.code,'',url)

    def parse_citation(self,single_citation):
        """Parses patent citation, returning results as a dictionary


        Returns (variables returned in dictionary, following are key names):  
            - patent_number (str)  : patent number
            - priority_date (str)  : priority date of patent
            - pub_date      (str)  : publication date of patent

        Inputs:
            - single_citation (str) : html string from citation section in google patent html

        """

        try:
            patent_number = single_citation.find('span',itemprop='publicationNumber').get_text()
        except:
            patent_number = ''
        # ~ Get priority date ~ #
        try:
            priority_date = single_citation.find('td',itemprop='priorityDate').get_text()
        except:
            priority_date = ''
        # ~ Get publication date ~ # 
        try:
            pub_date = single_citation.find('td',itemprop='publicationDate').get_text()
        except:
            pub_date
        return({'patent_number':patent_number,
                'priority_date':priority_date,
                'pub_date':pub_date})

    def process_patent_html(self,soup):
        """ Parse patent html using BeautifulSoup module


        Returns (variables returned in dictionary, following are key names): 
            - title                     (str)   : title
            - application_number        (str)   : application number
            - inventor_name             (json)  : inventors of patent 
            - assignee_name_orig        (json)  : original assignees to patent
            - assignee_name_current     (json)  : current assignees to patent
            - pub_date                  (str)   : publication date
            - filing_date               (str)   : filing date
            - priority_date             (str)   : priority date
            - grant_date                (str)   : grant date
            - expiration_date           (str)   : expiration date
            - forward_cites_no_family   (json)  : forward citations that are not family-to-family cites
            - forward_cites_yes_family  (json)  : forward citations that are family-to-family cites
            - backward_cites_no_family  (json)  : backward citations that are not family-to-family cites
            - backward_cites_yes_family (json)  : backward citations that are family-to-family cites

        Inputs:
            - soup (str) : html string from of google patent html
            

        """
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #  Get title 
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        title_text=''
        # Get title # 
        title = soup.find('meta',attrs={'name':'DC.title'})
        title_text=title['content'].rstrip()

        try:
            inventor_name = [{'inventor_name':x.get_text()} for x in soup.find_all('dd',itemprop='inventor')]
        except:
            inventor_name = []
        # Assignee #
        try:
            assignee_name_orig = [{'assignee_name':x.get_text()} for x in soup.find_all('dd',itemprop='assigneeOriginal')]
        except:
            assignee_name_orig = []
        try:
            assignee_name_current = [{'assignee_name':x.get_text()} for x in soup.find_all('dd',itemprop='assigneeCurrent')]
        except:
            assignee_name_current = []
          
        # Publication Date #
        try:
            pub_date = soup.find('dd',itemprop='publicationDate').get_text()
        except:
            pub_date = ''
        # Application Number #
        try: 
            application_number = soup.find('dd',itemprop="applicationNumber").get_text()
        except:
            application_number = ''
        # Filing Date # 
        try:
            filing_date = soup.find('dd',itemprop='filingDate').get_text()
        except:
            filing_date = ''
        # Loop through all events #
        list_of_application_events = soup.find_all('dd',itemprop='events')
        priority_date = ''
        grant_date = ''
        expiration_date = ''
        for app_event in list_of_application_events:
            # Get information #
            try:
                title_info = app_event.find('span',itemprop='type').get_text()
                timeevent = app_event.find('time',itemprop='date').get_text()
                if title_info == 'priority':
                    priority_date = timeevent
                if title_info == 'granted':
                    grant_date = timeevent
                if title_info == 'publication' and pub_date=='':
                    pub_date = timeevent
                if 'expiration' in app_event.find('span',itemprop='title').get_text().lower():
                    expiration_date = timeevent

            except:
                continue 

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #             Citations
        #
        # All citations are of the same format
        #   -Find all citations
        #   -If there are any citations, parse each individually using "parse_citation"
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        # ~~~ Forward Citations (No Family to Family) ~~~ #
        found_forward_cites_orig=soup.find_all('tr', itemprop="forwardReferencesOrig")
        forward_cites_no_family=[]
        if len(found_forward_cites_orig)>0:
            for citation in found_forward_cites_orig:
                forward_cites_no_family.append(self.parse_citation(citation))

        # ~~~ Forward Citations (Yes Family to Family) ~~~ #
        found_forward_cites_family=soup.find_all('tr', itemprop="forwardReferencesFamily")
        forward_cites_yes_family=[]
        if len(found_forward_cites_family)>0:
            for citation in found_forward_cites_family:
                forward_cites_yes_family.append(self.parse_citation(citation))

        # ~~~ Backward Citations (No Family to Family) ~~~ #
        found_backward_cites_orig = soup.find_all('tr', itemprop='backwardReferences')
        backward_cites_no_family=[]
        if len(found_backward_cites_orig)>0:
            for citation in found_backward_cites_orig:
                backward_cites_no_family.append(self.parse_citation(citation))

        # ~~~ Backward Citations (Yes Family to Family) ~~~ #
        found_backward_cites_family = soup.find_all('tr', itemprop='backwardReferencesFamily')
        backward_cites_yes_family=[]
        if len(found_backward_cites_family)>0:
            for citation in found_backward_cites_family:
                backward_cites_yes_family.append(self.parse_citation(citation))

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #  Get abstract 
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        abstract_text=''
        if self.return_abstract:
            # Get abstract # 
            abstract = soup.find('meta',attrs={'name':'DC.description'})
            # Get text 
            if abstract:
                abstract_text=abstract['content']

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        #  Return data as a dictionary
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
        return({'title': title_text,
                'inventor_name':json.dumps(inventor_name),
                'assignee_name_orig':json.dumps(assignee_name_orig),
                'assignee_name_current':json.dumps(assignee_name_current),
                'pub_date':pub_date,
                'priority_date':priority_date,
                'grant_date':grant_date,
                'filing_date':filing_date,
                'expiration_date': expiration_date,
                'forward_cite_no_family':json.dumps(forward_cites_no_family),
                'forward_cite_yes_family':json.dumps(forward_cites_yes_family),
                'backward_cite_no_family':json.dumps(backward_cites_no_family),
                'backward_cite_yes_family':json.dumps(backward_cites_yes_family),
                'abstract_text':abstract_text})

    def get_scraped_data(self,soup,patent,url):
        # ~~ Parse individual patent ~~ #
        parsing_individ_patent = self.process_patent_html(soup)
        # ~~ Add url + patent to dictionary ~~ #
        parsing_individ_patent['url'] = url
        parsing_individ_patent['patent'] = patent
        # ~~ Return patent info ~~ #
        return(parsing_individ_patent)


    def scrape_all_patents(self):
        """ Scrapes all patents in list self.list_of_patents using function "request_single_patent". 

        If you want to scrape a single patent without adding it to the class variable, 
            use "request_single_patent" function as a method on the class. See the doc string
            in the class module for an example.

        """
        # ~ Check if there are any patents ~ #
        if len(self.list_of_patents)==0:
            raise(NoPatentsError("no patents to scrape specified in 'patent' variable: add patent using class.add_patents([<PATENTNUMBER>])"))
        # ~ Loop through list of patents and scrape them ~ #
        else:
            for patent in self.list_of_patents:
                error_status, soup, url = self.request_single_patent(patent)
                # ~ Add scrape status variable ~ #
                self.add_scrape_status(patent,error_status)
                if error_status=='Success':
                    self.parsed_patents[patent] = self.get_scraped_data(soup,patent,url)
                else:
                    self.parsed_patents[patent] = {}




