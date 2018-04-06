"""
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""



class FPLogger(object):
    
    """ Singleton logger class 
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FPLogger, cls).__init__(cls, *args, **kwargs)
        
        return cls._instance
            
            
    def __init__(self):
        print("called")
        
        