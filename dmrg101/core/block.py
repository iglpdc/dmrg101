# 
# File: block.py
# Author: Ivan Gonzalez
#
""" A module for blocks.
"""
import copy 
import numpy as np
from dmrg101.core.dmrg_exceptions import DMRGException
from dmrg101.core.sites import Site

class Block(Site):
    """A block.
    
    That is the representation of the Hilbert space and operators of a
    direct product of single site's Hilbert space and operators, that have
    been truncated.
    
    You use this class to create the two blocks (one for the left, one for
    the right) needed in the DMRG algorithm. The block comes empty.

    Parameters
    ----------
    dim : an int.
	Size of the Hilbert space. The dimension must be at least 1. A
	block of dim = 1  represents the vaccum (or something strange like
	that, it's used for demo purposes mostly.)
    operators : a dictionary of string and numpy array (with ndim = 2).
	Operators for the block.

    Examples
    --------
    >>> from dmrg101.core.block import Block
    >>> brand_new_block = Block(2)
    >>> # the Hilbert space has dimension 2
    >>> print brand_new_block.dim
    2
    >>> # the only operator is the identity
    >>> print brand_new_block.operators
    {'id': array([[ 1.,  0.],
           [ 0.,  1.]])}
    """
    def __init__(self, dim):
    	"""Creates an empty block of dimension dim.
    
	Raises
	------
	DMRGException
	     if `dim` < 1.

	Notes	
	-----
	Postcond : The identity operator (ones in the diagonal, zeros elsewhere)
	is added to the `self.operators` dictionary. A full of zeros block
	Hamiltonian operator is added to the list.
    	"""
    	super(Block, self).__init__(dim)

def make_block_from_site(site):
    """Makes a brand new block using a single site.

    You use this function at the beginning of the DMRG algorithm to
    upgrade a single site to a block.

    Parameters
    ----------
    site : a Site object.
        The site you want to upgrade.
    
    Returns
    -------
    result: a Block object.
        A brand new block with the same contents that the single site.

    Postcond
    --------
    The list for the operators in the site and the block are copied,
    meaning that the list are different and modifying the block won't
    modify the site.

    Examples
    --------
    >>> from dmrg101.core.block import Block
    >>> from dmrg101.core.block import make_block_from_site 
    >>> from dmrg101.core.sites import SpinOneHalfSite
    >>> spin_one_half_site = SpinOneHalfSite()
    >>> brand_new_block = make_block_from_site(spin_one_half_site)
    >>> # check all it's what you expected
    >>> print brand_new_block.dim
    2
    >>> print brand_new_block.operators.keys()
    ['s_p', 's_z', 's_m', 'id']
    >>> print brand_new_block.operators['s_z']
    [[-0.5  0. ]
     [ 0.   0.5]]
    >>> print brand_new_block.operators['s_p']
    [[ 0.  0.]
     [ 1.  0.]]
    >>> print brand_new_block.operators['s_m']
    [[ 0.  1.]
     [ 0.  0.]]
    >>> # operators for site and block are different objects
    >>> print ( id(spin_one_half_site.operators['s_z']) == 
    ...		id(brand_new_block.operators['s_z']) )
    False
    """
    result = Block(site.dim)
    result.operators = copy.deepcopy(site.operators)
    return result
