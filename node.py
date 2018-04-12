"""
__file__ = "fpgrowth.py"
__author__ = "Vishal Jasrotia"
__credits__ = ["Vishal Jasrotia"]
__version__ = "1.0.1"
__maintainer__ = "Vishal Jasrotia"
__email__ = "jasrotia.vishal@stonybrook.edu
__status__ = "In Progress"
"""

class Node:
    """ FP tree node single node class
    """
    
    def __init__(self, val ,  count = 0):
        self.val = val
        self.count = count
        self.childrens = []
        self.neighbour = None
    
    def __str__(self):
        return "{0}, count : {1}, neighbour :({2}), childrens :{3}".format(self.val, self.count, self.neighbour, self.childrens)
        
    
    