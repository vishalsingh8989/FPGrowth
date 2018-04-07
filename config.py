"""
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""

import os
from singleton import Singleton


@Singleton
class Config:
    """ intialize config related params
    """
    
    def __init__(self):
        self.root = os.getcwd()
        
        
    