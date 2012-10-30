'''
File: exceptions.py
Author: Ivan Gonzalez
Description: Exception class for the DMRG code
'''
class DMRGException(Exception):
    """A base exception for the DMRG code
    
    Attributes:
        msg: a string with a message explaining the error
    """
    def __init__(self, msg):
    	super(DMRGException, self).__init__()
    	self.msg = msg
    
    def __srt__(self, msg):
    	return repr(self.msg)
