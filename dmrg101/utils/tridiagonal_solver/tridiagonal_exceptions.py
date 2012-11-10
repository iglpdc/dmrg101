# 
# File: tridiagonal_exceptions.py
# Author: Ivan Gonzalez
# 
"""Exception class for the tridiagonal module
"""
class TridiagonalException(Exception):
    """A base exception for the Tridiagonal module
    
    Parameters
    ----------
    msg : a string 
        A message explaining the error
    """
    def __init__(self, msg):
    	super(TridiagonalException, self).__init__()
    	self.msg = msg
    
    def __srt__(self, msg):
    	return repr(self.msg)
