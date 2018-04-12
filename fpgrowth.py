"""
__file__ = "fpgrowth.py"
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""

import os
import sys
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
        self._invalid_attr = ["0.0", "null", 0.0]
        
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0}  input_file = {1} ,  min_sup = {2}".format(self, input_file, min_sup))
        self._min_support = min_sup
        self._input_file = input_file
        if self._input_file.endswith(".csv"):
            self._df = pd.read_csv(os.path.join(self._config.root , "input", self._input_file)) 
        elif self._input_file.endswith(".xlsx"):
            self._df = pd.read_excel(os.path.join(self._config.root , "input", self._input_file))
        else:
            self.log.error("File type {0} is not supported. Only csv and xslx file supported.".format(self._input_file.split(".")[1]))
        
        self._df = self._df[:10]
        self.log.debug("shape :  {0}".format(self._df.shape))
    
    
    
    def frequent_itemset(self):
        """ find frequent pattern
        @param None: 
        """
        
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0} )".format(self))
        
        self._attr_freq_table = {}
        self._dropped = {}
        self.log.info("Generate items freq table.")
        for column in self._df.columns:
            for attr, count in self._df[column].value_counts().iteritems():
                if count >  self._min_support and attr not in self._invalid_attr:
                    self._attr_freq_table[attr] = count
        self.log.info("Items with frequency more than min_sup : {0}.".format(self._min_support))
        self.log.info(self._attr_freq_table)
        self._item_support = sorted(self._attr_freq_table.items(), key=lambda x: x[1])
  
        self._item_support_list  = [item[0] for item in self._item_support]
        self._item_support_list.reverse()
        
        self.log.info("Ordered item set : ")
        self._item_support.reverse()
        self.log.info(self._item_support())
        
        self.log.info("Items :")
        self.log.info(self._item_support_list)
        
        self._ordered_items = self.extract_ordered_items(self._df, self._item_support_list)
        
        self.supported_item_count = {}
        for transaction_id, ordered_set in self._ordered_items.iteritems():
            for item in ordered_set:
                self.supported_item_count[item] = self.supported_item_count.get(item, 0) + 1
        
        self.log.info("Supported item count in ordered set:")
        self.log.info(self.supported_item_count)
                
        
        
                
    def extract_ordered_items(self, df, support_list):
        """
        extract ordered items from data frame
        @param df: pandas Dataframe
        @param support_list: list of supported in reverse order for freq. 
        @rtype: dict of transaction id ves order item set
        """
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0} , df = {1} ,  support_list = {2})".format(self, df.shape, support_list))
        
        ordered_items = {}
        for row in self._df.iterrows():
            item_list = []
            row_list = list(row[1])
            for item in support_list:
                if item in row_list:
                    item_list.append(item)
            ordered_items[row[0]] = item_list
            self.log.info("Transaction id: {0} , Ordered Items : {1}".format(row[0],item_list))
           
           
        self.log.info("Transaction vs Ordered Items set")     
        self.log.info(ordered_items)
        
        return ordered_items










    
    
    
    
    


