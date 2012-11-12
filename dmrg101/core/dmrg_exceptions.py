# 
# File: dmrg_exceptions.py
# Author: Ivan Gonzalez
# 
"""Exception class for the DMRG code
"""
class DMRGException(Exception):
    """A base exception for the DMRG code
    
    Parameters
    ----------
    msg : a string 
        A message explaining the error
    """
    def __init__(self, msg):
    	super(DMRGException, self).__init__()
    	self.msg = msg
    
    def __srt__(self, msg):
    	return repr(self.msg)
