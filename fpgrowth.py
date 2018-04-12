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
"""
__file__ = "fpgrowth.py"
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""

import time
import logging
import pandas as pd

from fplogger import FPLogger
from config import Config


DEBUG = True

class FPGrowth:
    """ FP Growth algorithm : https://dl.acm.org/citation.cfm?doid=335191.335372
    """
    _name = "FPGrowth"
    
    def __init__(self, input_file, min_sup):
        """
        """
        self.log = FPLogger()
        self._config = Config()
        
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0}  input_file = {1} ,  min_sup = {2}".format(self, input_file, min_sup))
        self._min_support = min_sup
        self._input_file = input_file
        if self._input_file.endswith(".csv"):
            self._df = pd.read_csv(os.path.join(self._config.root , "input", self._input_file)) 
        elif self._input_file.endswith(".xlsx"):
            self._df = pd.read_excel(os.path.join(self._config.root , "input", self._input_file))
        #print(self._df)
        self.log.debug("shape :  {0}".format(self._df.shape))
    
    def find_frequent_itemset(self):
        """ find frequent pattern
        @param None: 
        """
        
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0} )")
        
        self._attr_freq_table = {}
        self._dropped = {}
        for column in self._df.columns:
            for attr, count in self._df[column].value_counts().iteritems():
                if count >  self._min_support:
                    self._attr_freq_table[attr] = count
        self.log.info(self._attr_freq_table)
        
                
        











    
    
    
    
    


