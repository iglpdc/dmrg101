'''
File: wavefunction.py
Author: Ivan Gonzalez
Description: The class for wavefunctions
'''
import numpy as np
from dmrg_exceptions import DMRGException
from braket import braket

class Wavefunction(object):
    """A wavefunction object
    
    You use this class to represent wavefunctions. Wavefunctions are
    stored as matrices, the rows corresponding to the states of the
    left block, and the columns corresponding to the states of the
    right block. 
    
    Parameters
    ----------
        left_dim: an int with the dimension of the Hilbert space of the left block
        right_dim: an int with the dimension of the Hilbert space of the right block
	num_type: a type (double, complex) with the type of the
	    wavefunction matrix elements.
    """
    def __init__(self, left_dim, right_dim, num_type='double'):
    	"""Creates an empty wavefunction
    
    	The wavefunction has the correct dimensions, but their
    	contents are garbage. You *must* give it a value before use it for
	any calculation.
    
    	Raises
	------
    	    DMRGException: if the left_dim, right_dim are not
    	    integers.
    	"""
    	super(Wavefunction, self).__init__()
    	try:
    	    self.as_matrix = np.empty((left_dim, right_dim), 
    				       num_type)
    	except TypeError:
    	    raise DMRGException("Bad args for wavefunction")
    	self.left_dim = left_dim
    	self.right_dim = right_dim

    def build_reduced_density_matrix(self, block_to_be_traced_over):
	"""Constructs the reduced DM for this wavefunction.

	You use this function to build the reduced density matrix of this
	wavefunction. The reduced DM is itself a square and hermitian
	matrix as it should.

	Parameters
	----------
	    block_to_be_traced_over: a string with which block (left or
	    right) will be traced over.

 	Returns
	-------
	    a square and hermitian matrix with the reduced DM.

        Raises
	------
	    DMRGException if the name for the block to be traced out is 
	        not correct
	"""
	if block_to_be_traced_over not in ('left', 'right'):
	    raise DMRGException("block_to_be_traced_over must be left
	 		         or right")
	
	result=np.array(self.as_matrix.dtype.name)

	if (block_to_be_traced_over == 'left'):
	    result = np.dot(np.transpose(self.as_matrix), self.as_matrix)
	else:
	    result = np.dot(self.as_matrix, np.transpose(self.as_matrix))
	return result

    def get_norm(self):
	""" Calculates the norm of a wavefunction

	Simply uses the braket function to calculate the norm.
	The wavefunction is *unchanged* upon calculation. Use normalize if
	you want to normalize the wavefunction.

	Returns
	-------
	    a double with the norm of the wavefunction
	"""
	norm_squared=braket(self, self)

	# get rid of the complex part, which should be 0.0, for complex wfs
	if self.as_matrix.iscomplexobj():
	    norm_squared=double(norm_squared.real)

	return sqrt(norm_squared)

    def normalize(self):
	""" Normalizes the wavefunction

	Postcond
	--------
	    The wavefunction is normalized, i.e. changes to have norm
	    1.0.

	Raises
	------
	    DMRGException: if the norm of the wavefunction is zero.
	"""
	try:
	    self.as_matrix/=get_norm(self)
	except ValueError:
	    raise DMRGException("Wavefunction norm is zero")

    def randomize(self):
	"""Fills the wavefunction with random values and normalizes.

	You use this function to generate a random wavefunction, i.e. one
	whose elements are random number. The wavefunction is normalized.
	The old elements of the wavefunction (if there were any) are
	lost after using this function.

	Postcond
	--------
	    The wavefunction is filled with random elements and has norm
	    1.0.
	"""
	self.as_matrix=np.random(self.left_dim, self.right_dim)
	self.normalize()
