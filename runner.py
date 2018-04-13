"""
__file__ = "runner.py"
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
from fpgrowth import FPGrowth
from config import Config
from optparse import OptionParser


def set_up_environment():
    if "output" not in os.listdir(os.getcwd()):
        print("Create output folder...")
        output_path = os.path.join(os.getcwd(), "output")
        try:
            os.mkdir(output_path)
        except OSError as err:
            print("Error in creating output folder : {0} : {1}".format(output_path, err))
        if "output" not in os.listdir(os.getcwd()):
            print("Error in creating output folder : ", output_path)
            exit()
        else:
            print("Output folder created : {0}".format(output_path))
        
        print("Add {0} to env.".format(os.getcwd()))
    print("Environment set up succussful")
        
        


if __name__ == "__main__":
    set_up_environment()
    config = Config()
    
    
    args = OptionParser(usage='% prog data_file')
    args.add_option('-m', '--minimum-support', dest='minimum_support', type='int')
    args.add_option('-f', '--file', dest='file_name', type='string')
    args.set_defaults(minimum_support=150)
    
    options, args = args.parse_args()

    if options.file_name.endswith(".csv") or options.file_name.endswith(".xlsx")  or options.file_name.endswith(".data"):
        pass
    else:
        print("csv or xlsx file required.")
        exit()
        
    
    fpg = FPGrowth(options.file_name, options.minimum_support)
    fpg.frequent_itemset()
    
    
    print("Done..")




