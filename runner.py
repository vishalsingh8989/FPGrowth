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
from fpgrowth import FPGrowth
from config import Config



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
    
    print("Choose input file:")
    input_files = []
    for file_name in os.listdir(os.path.join(config.root, "input")):
        if file_name.endswith(".csv")  or file_name.endswith(".data"):
            input_files.append(file_name)

    print("******************************")
    print("****   INPUT FILES    ********")
    print("******************************")
    for i, file_name in enumerate(input_files,1):
        print("{0} :  {1}".format(i, file_name))
    print("******************************")
    print("Enter your choice : ")
    file_num = int(input()) - 1
    
    if file_num >=0  and file_num < len(input_files):
        print("Input file : {0}".format(input_files[file_num]))
    else:
        print("Invalid file number. exit.")
        exit()
    
    
    fpg = FPGrowth(input_files[file_num])
    fpg.find_frequent_itemset()
    
    
    
    print("Done..")




