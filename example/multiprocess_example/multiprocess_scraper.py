# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# This script describes how to scrape multiple 
#  patents using python's multiprocessing module.
#  The scripts example patents are shown in list_of_patents, and
#  are a subset of patents from Thomas Alva Edison.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

# ~~~~~~~~~~~~~~~~~ #
# ~~~ Libraries ~~~ #
# ~~~~~~~~~~~~~~~~~ #

# ~ Script specific ~ #
from functions import *

# ~ Multiprocessing ~ #
from functools import partial
import multiprocessing as mp

# ~ System ~ #
import os


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~ Sample of patents from Thomas Alva Edison ~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

list_of_patents = ['CH2881A', 'CH2000A', 'AU403812A', 
                   'US1398011A', 'US223898A', 'US3921137A', 
                   'US692507A', 'US1127028A', 'US821625A', 
                   'AT20010B', 'AT19461B', 'FR386001A', 
                   'AT9157B', 'AT33940B', 'AT35596B', 
                   'AT23979B', 'AT26781B', 'AT37077B', 
                   'AT9095B', 'AT26782B', 'AT24256B', 
                   'AT7459B', 'AT26856B', 'AT22264B', 
                   'AT35605B', 'AT7130B', 'AT35857B', 
                   'AT35609B', 'AT20868B', 'CA41891A', 
                   'GB190013693A', 'FR348747A', 'FR328291A', 
                   'FR362692A', 'FR362691A', 'CA130636A']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~~ Parameters for data file ~~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
path_to_data = 'path_to_data'


## Create csv file to store the data from the patent runs 
#  (1) Specify column order of patents
#  (2) Create csv if it does not exist in the data path
data_column_order = ['inventor_name',
                    'assignee_name_orig',
                    'assignee_name_current',
                    'pub_date',
                    'priority_date',
                    'grant_date',
                    'filing_date',
                    'forward_cite_no_family',
                    'forward_cite_yes_family',
                    'backward_cite_no_family',
                    'backward_cite_yes_family',
                    'url',
                    'patent']
if 'edison_patents.csv' not in os.listdir(path_to_data):
    with open(path_to_data + 'edison_patents.csv','w',newline='') as ofile:
        writer = csv.writer(ofile)
        writer.writerow(data_column_order)

########### Run pool process #############
if __name__ == "__main__":

    ## Create lock to prevent collisions when processes try to write on same file 
    l = mp.Lock()    

    ## Use a pool of workers where the number of processes is equal to 
    ##   the number of cpus - 1 
    with poolcontext(processes=mp.cpu_count()-1,initializer=init,initargs=(l,)) as pool:
        pool.map(partial(single_process_scraper,path_to_data_file=path_to_data + 'edison_patents.csv',
                                                data_column_order=data_column_order),
                                                list_of_patents)
