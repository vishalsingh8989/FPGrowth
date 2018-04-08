"""
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""


import os
import sys
import time
import logging
import pandas as pd

from fplogger import FPLogger
from config import Config

class FPGrowth:
    """ FP Growth algorithm : https://dl.acm.org/citation.cfm?doid=335191.335372
    """
    
    def __init__(self, input_file):
        self.log = FPLogger()
        self._config = Config()
        self._input_file = input_file
        self._df = pd.read_csv(os.path.join(self._config.root , "input", input_file))    
        self.log.debug(self._df)
        
        self.log.debug("shape :  {0}".format(self._df.shape))
    
    def find_frequent_itemset(self):
        pass
        











    
    
    
    
    


