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
import itertools
import pandas as pd

from fplogger import FPLogger
from config import Config
from node import Node
import node

DEBUG = False

class FPGrowth:
    """ FP Growth algorithm : https://dl.acm.org/citation.cfm?doid=335191.335372
    """
    _name = "FPGrowth"
    
    def __init__(self, input_file, min_sup):
        """
        """
        self.log = FPLogger()
        self._config = Config()
        self._invalid_attr = ["null"]
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
        
        
        
        #self._df = self._df[:25]
        print(self._df)
        self.log.debug("shape :  {0}".format(self._df.shape))
    
    
    
    def frequent_itemset(self):
        """ find frequent pattern
        @param None: 
        """
        
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0} )".format(self))
        
        self._table = {}
        self._attr_freq_table = {}
        self._dropped = {}
        self.log.info("Generate items freq table.")
        for row in self._df.iterrows():
            for val in row[1]:
                if val not in self._invalid_attr:
                    self._table[val] = self._table.get(val, 0) + 1
        
        for key , val in self._table.iteritems():
            if val > self._min_support:
                self._attr_freq_table[key] = val
                
        for key , val in self._attr_freq_table.iteritems():
            self.log.debug(key)
            self.log.debug(val)
        self.log.info("Items with frequency more than min_sup : {0}.".format(self._min_support))
        self.log.info(self._attr_freq_table)
        self._item_support = sorted(self._attr_freq_table.items(), key=lambda x: x[1])
  
        self._item_support_list  = [item[0] for item in self._item_support]
        self._item_support_list.reverse()
        self.log.info("Ordered item set : ")
        self._item_support.reverse()
        self.log.info(self._item_support)
        
        self.log.info("Items :")
        self.log.info(self._item_support_list)    
        self._ordered_items = self.extract_ordered_items(self._df, self._item_support_list)
    
        self.supported_item_count = {}
        for transaction_id, ordered_set in self._ordered_items.iteritems():
            for item in ordered_set:
                self.supported_item_count[item] = self.supported_item_count.get(item, 0) + 1
        
        self.log.info("Supported item count in ordered set: {0}".format(self.supported_item_count))
        self.header_table = []
        for attr, freq in self._item_support:
            table_row = [attr, freq, None]
            self.header_table.append(table_row)
        
        self.log.info("Header table for FP Tree : {0}".format(self.header_table))
        self.header_table, self.fptree_root = self.make_fp_tree(self.header_table, self._ordered_items)
        
        
        self.log.info("Root node : {0}".format(self.fptree_root))
        self.log.info("Header table for FPTree")
        for row in self.header_table:
            self.log.info(row)
        
        self.conditional_pattern_base = {}
        self.log.debug("Generate conditional pattern base:")
        self.generate_conditional_pattern_base(self.fptree_root, self.conditional_pattern_base , [])
        
        #self.log.debug(self.conditional_pattern_base)
        
        
        self.conditional_pattern_tree_count,self.conditional_pattern_tree = self.generate_conditional_pattern_tree(self.conditional_pattern_base)
        self.log.debug("****************************")
        self.log.debug("Frequent pattern items:")
        
        for key, val in self.conditional_pattern_tree.iteritems():    
            self.log.debug("[ " + str(key) + "] : " + str(self.conditional_pattern_tree_count[key]))
            for size in xrange(1,len(val)+1):
                attr_list = list(itertools.combinations(val.keys(), size))
                for freq_pattern in attr_list:
                    count = min([ val[k] for k in freq_pattern]) 
                    freq_pattern = list(freq_pattern) + [key]
                    self.log.debug(str(freq_pattern) + " : " + str(count))
               
     
    def generate_conditional_pattern_tree(self, conditional_pattern_base):
        """ Generate condition pattern tree using pattern base
        @param conditional_pattern_base: dict od attr vs tuple vs count
        """
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0}, conditional_pattern_base = {1} )".format(self, conditional_pattern_base))
        conditional_pattern_tree = {}
        conditional_pattern_tree_count = {}
        for key, val  in conditional_pattern_base.iteritems():
            cache = {}
            count = 0
            for association, c  in val.iteritems():
                for item in association:
                    cache[item] = cache.get(item, 0) + c
                count += c
            reduced = {}
            for k, v in cache.iteritems():
                if v >  self._min_support:
                    reduced[k] = v
            if len(reduced) > 0 :
                count = min([v for k,v in reduced.iteritems()])
            else:
                count = count
            conditional_pattern_tree[key] = reduced
            conditional_pattern_tree_count[key] = count
        return conditional_pattern_tree_count, conditional_pattern_tree, 


        
    def generate_conditional_pattern_base(self, root , conditional_pattern_base, ancestors_list, indt =  "|-->"):
        """
        Generate conditinal pattern base.
        
        """
        if root is not None:
            if root.val != "NULL":
                if conditional_pattern_base.get(root.val, None) is None:
                    conditional_pattern_base[root.val] = {tuple(ancestors_list) : root.count}
                else:
                    conditional_pattern_base[root.val][tuple(ancestors_list)] = root.count
                ancestors_list.append(root.val)
        
            for child in root.childrens:
                self.generate_conditional_pattern_base(child, conditional_pattern_base, ancestors_list, indt + "|-->")
            
            if root.val != "NULL":
                ancestors_list.pop()
        
        
    def make_fp_tree(self, header_table, ordered_set):
        """Make FP tree.
        @param header_table: Header table for FPtree links 
        @param ordered_set: Ordered set
        """
        if DEBUG:
            self.log.debug(sys._getframe().f_code.co_name + "(self = {0},\n header_table = {1},\n ordered_set = {2})".format(self, header_table, ordered_set))
        
        fp_tree = Node("NULL", 1)
        for transaction_id, ordered_set in self._ordered_items.iteritems():
            curr_node = fp_tree
            if len(ordered_set) == 0:
                continue
            last_node_exist = False
            for attr in ordered_set:
                if self.find_child(curr_node, attr):
                    curr_node.count = curr_node.count +  1
                    curr_node = self.find_child(curr_node, attr)
                    last_node_exist = True
                else:
                    node = Node(attr, 1)
                    if len(curr_node.childrens) > 0  or last_node_exist:
                        curr_node.count  =  curr_node.count + 1
                    curr_node.childrens.append(node)
                    self.link_header_table(header_table, node)
                    curr_node = node
                    last_node_exist = False
            
            if last_node_exist:
                curr_node.count = curr_node.count +  1

        return header_table, fp_tree
                
                    
    def find_child(self, curr_node, attr):
        """
        """
        for child in curr_node.childrens:
            if child.val == attr:
                return child
        return None 
                    
                
    def link_header_table(self, header_table, node):
        """
        Link header table entries and link FPTree. 
        @param header_table: Header table for FPtree links 
        @param ordered_set: Ordered set        
        """
        
        #if DEBUG:
        #    self.log.debug(sys._getframe().f_code.co_name + "(self = {0} , header_table = {1}, node = {2})".format(self, header_table, node))
        
        for row in header_table:
            if row[0] == node.val:
                if row[2] is None:
                    row[2] = node
                else:
                    curr_node = row[2]
                    while curr_node.neighbour is not None:
                        curr_node =  curr_node.neighbour 
                    curr_node.neighbour = node        
        
        
                
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
           
           
        #self.log.info("Transaction vs Ordered Items set")     
        #self.log.info(ordered_items)
        
        return ordered_items










    
    
    
    
    


