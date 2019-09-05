
# ~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~ Import libraries ~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~ #

# Google Scraper Class #
from google_patent_scraper import scraper_class

# Context Manager #
from contextlib import contextmanager

# Writing/Reading #
import csv

# Multiprocessing #
import multiprocessing as mp



# ~~~~~~~~~~~~~~~~~~~ #
# ~~~~ Functions ~~~~ #
# ~~~~~~~~~~~~~~~~~~~ #

def single_process_scraper(patent,path_to_data_file,data_column_order):
    """Scrapes a single google patent using the google scraper class
       
       Function does not return any values, instead it writes the output
         of the data into a csv file specified in the path_to_data_file
         parameter

       Inputs:
         patent (str) : patent number including country prefix
         lock (obj) : to prevent collisions, function uses a lock. You can pass whichever
                      lock you want to this parameter
         path_to_data_file : absolute path to csv file to write data to
         data_column_order : name of columns in order they will be saved in csv file

    """
    # ~ Initialize scraper class ~ #
    scraper=scraper_class() 

    # ~ Scrape single patent ~ #
    err, soup, url = scraper.request_single_patent(patent)

    # Checks if the scrape is successful.
    # If successful -> parse text and deposit into csv file
    # Else          -> print error statement

    if err=='Success':
        patent_parsed = scraper.get_scraped_data(soup,url,patent)

        # Save the parsed data to a csv file 
        #  using multiprocessing lock function
        #  to prevent collisions
        with lock:
            with open(path_to_data_file,'a',newline='') as ofile:
                writer = csv.DictWriter(ofile, fieldnames=data_column_order)
                writer.writerow(patent_parsed)
    else:
        print('Patent {0} has error code {1}'.format(patent,err))

# Allow pool to accept keyword arguments
@contextmanager
def poolcontext(*args, **kwargs):
    pool = mp.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

def init(l):
    """Creates lock object that is global, for use in sharing 
       across processes
    """
    global lock
    lock = l