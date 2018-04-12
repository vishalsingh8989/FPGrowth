"""
__file__ = "fplogger.py"
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

from config import Config
from singleton import Singleton

@Singleton
class FPLogger(object):
    
    """ Singleton logger class for all logging.
    """
            
    def __init__(self):
        """
        """

        self._logger = logging.getLogger(name="FPGrowth")
        self._config = Config()
        
        #print output on terminal-> stdout
        self._streamHandler = logging.StreamHandler(sys.stdout)
        
        #create file handler for saving logs
        self._output_folder = os.path.join(self._config.root ,"output" , "FPGrowth_" + "_".join(time.ctime().split()[1:]))        
        try:
            os.mkdir(self._output_folder)
        except OSError as err:
            print("Error in creating output folder for logs and results. {0}".format(err))
            exit()
        self._log_file_path = os.path.join(self._output_folder , "FPGrowth.log")
        self._fileHandler = logging.FileHandler(self._log_file_path)
        
        
        # add _fileHandler and _streamHandler(stdout) to logger obj.
        self._logger.addHandler(self._fileHandler)
        self._logger.addHandler(self._streamHandler)
        
        #log _formatter
        self._formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # set _formatter  on both streams
        self._fileHandler.setFormatter(self._formatter)
        self._streamHandler.setFormatter(self._formatter)
        
        #debug level
        self._logger.setLevel(logging.DEBUG)
#         self._logger.info("Logging info")
#         self._logger.debug("Logging debug")
#         self._logger.error("Logging error")
    
    
    def info(self, msg):
        """ logger function for info msg
        """
        self._logger.info(msg)
    
    def debug(self, msg):
        """logger function for debug msg
        """
        self._logger.debug(msg)
        
    def error(self, msg):
        """logger function for error msg
        """
        self._logger.error(msg)
        
        
        
        

        
        
        
        