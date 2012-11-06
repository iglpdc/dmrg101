# 
# File: sites.py
# Author: Ivan Gonzalez
#
""" A module for single sites.
"""
from numpy import zeros, eye
from dmrg_exceptions import DMRGException

class Site(object):
    """A general single site
    
    You use this class to create a single site. The site comes empty (i.e.
    with no operators included), but for th identity operator. You should
    add operators you need to make you site up.
    
    Parameters
    ----------
    dim : an int 
	Size of the Hilbert space. The dimension must be at least 1. A site of
        dim = 1  represents the vaccum (or something strange like that, it's
        used for demo purposes mostly.)
    operators : dictionary of string and ndarray (with ndim = 2)
	Operators for the site.

    Examples
    --------
    >>> from dmrg101.core.sites import Site
    >>> brand_new_site = Site(2)
    >>> # the Hilbert space has dimension 2
    >>> print brand_new_site.dim
    2
    >>> # the only operator is the identity
    >>> print brand_new_site.operators
    {'id': array([[ 1.,  0.],
           [ 0.,  1.]])}
    """
    def __init__(self, dim):
    	"""Creates an empty site of dimension dim.
    
	Raises
	------
	DMRGException
	     if `dim` < 1.

	Notes	
	-----
	Postcond : The identity operator (ones in the diagonal, zeros elsewhere)
	is added to the `self.operators` dictionary.
    	"""
    	if dim < 1:
    	    raise DMRGException("Site dim must be at least 1")
    	super(Site, self).__init__()
    	self.dim = dim
	self.operators={ "id" : eye(self.dim, self.dim) }
    
    def add_operator(self, operator_name):
    	"""Adds an operator to the site
    
    	Parameters
	----------
    	operator_name : string
	    The operator name.

	Raises
	------
	DMRGException 
	    if `operator_name` is already in the dict.
	    
	Notes
	-----
	Postcond:

        - `self.operators` has one item more, and
        - the newly created operator is a (`self.dim`, `self.dim`)
          matrix of full of zeros.
	
	Examples
	--------
	>>> from dmrg101.core.sites import Site
	>>> new_site = Site(2)
	>>> print new_site.operators.keys()
	['id']
	>>> new_site.add_operator('s_z')
	>>> print new_site.operators.keys()
	['s_z', 'id']
	>>> # note that the newly created op has all zeros
	>>> print new_site.operators['s_z']
	[[ 0.  0.]
	 [ 0.  0.]]
        """
	if str(operator_name) in self.operators.keys():
    	    raise DMRGException("Operator name exists already")
    	else:
    	    self.operators[str(operator_name)] = zeros((self.dim, self.dim))


class SpinOneHalfSite(Site):
    """A site for spin 1/2 models.
    
    You use this site for models where the single sites are spin
    one-half sites. The Hilbert space is ordered such as the first state
    is the spin down, and the second state is the spin up. Therefore e.g.
    you have the following relation between operator matrix elements:

    .. math::
        \langle \downarrow \left| A \\right|\uparrow \\rangle = A_{0,1}

    Notes
    -----
    Postcond : The site has already built-in the spin operators for s_z, s_p, s_m.

    Examples
    --------
    >>> from dmrg101.core.sites import SpinOneHalfSite
    >>> spin_one_half_site = SpinOneHalfSite()
    >>> # check all it's what you expected
    >>> print spin_one_half_site.dim
    2
    >>> print spin_one_half_site.operators.keys()
    ['s_p', 's_z', 's_m', 'id']
    >>> print spin_one_half_site.operators['s_z']
    [[-1.  0.]
     [ 0.  1.]]
    >>> print spin_one_half_site.operators['s_p']
    [[ 0.  0.]
     [ 1.  0.]]
    >>> print spin_one_half_site.operators['s_m']
    [[ 0.  1.]
     [ 0.  0.]]
    """
    def __init__(self):
	"""Creates the spin one-half site.

	Notes
	-----
	Postcond : the dimension is set to 2, and the Pauli matrices
	are added as operators.
	"""
        super(SpinOneHalfSite, self).__init__(2)
	# add the operators
        self.add_operator("s_z")
        self.add_operator("s_p")
        self.add_operator("s_m")
	# for clarity
        s_z = self.operators["s_z"]
        s_p = self.operators["s_p"]
        s_m = self.operators["s_m"]
	# set the matrix elements different from zero to the right values
        s_z[0, 0] = -1.0
        s_z[1, 1] = 1.0
        s_p[1, 0] = 1.0
        s_m[0, 1] = 1.0


class ElectronicSite(Site):
    """A site for electronic models
    
    You use this site for models where the single sites are electron
    sites. The Hilbert space is ordered such as:

    - the first state, labelled 0,  is the empty site,
    - the second, labelled 1, is spin down, 
    - the third, labelled 2, is spin up, and 
    - the fourth, labelled 3, is double occupancy.
    
    Notes
    -----
    Postcond: The site has already built-in the spin operators for: 

    - c_up : destroys an spin up electron,
    - c_up_dag, creates an spin up electron,
    - c_down, destroys an spin down electron,
    - c_down_dag, creates an spin down electron,
    - s_z, component z of spin,
    - s_p, raises the component z of spin,
    - s_m, lowers the component z of spin,
    - n_up, number of electrons with spin up,
    - n_down, number of electrons with spin down,
    - n, number of electrons, i.e. n_up+n_down, and
    - u, number of double occupancies, i.e. n_up*n_down.

    Examples
    --------
    >>> from dmrg101.core.sites import ElectronicSite
    >>> hubbard_site = ElectronicSite()
    >>> # check all it's what you expected
    >>> print hubbard_site.dim
    4
    >>> print hubbard_site.operators.keys() # doctest: +ELLIPSIS
    ['s_p', ...]
    >>> print hubbard_site.operators['n_down']
    [[ 0.  0.  0.  0.]
     [ 0.  1.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  1.]]
    >>> print hubbard_site.operators['n_up']
    [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  1.  0.]
     [ 0.  0.  0.  1.]]
    >>> print hubbard_site.operators['u']
    [[ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  0.]
     [ 0.  0.  0.  1.]]
    """
    def __init__(self):
        super(ElectronicSite, self).__init__(4)
	# add the operators
        self.add_operator("c_up")
        self.add_operator("c_up_dag")
        self.add_operator("c_down")
        self.add_operator("c_down_dag")
        self.add_operator("s_z")
        self.add_operator("s_p")
        self.add_operator("s_m")
        self.add_operator("n_up")
        self.add_operator("n_down")
        self.add_operator("n")
        self.add_operator("u")
	# for clarity
        c_up = self.operators["c_up"]
        c_up_dag = self.operators["c_up_dag"]
        c_down = self.operators["c_down"]
        c_down_dag = self.operators["c_down_dag"]
        s_z = self.operators["s_z"]
        s_p = self.operators["s_p"]
        s_m = self.operators["s_m"]
        n_up = self.operators["n_up"]
        n_down = self.operators["n_down"]
        n = self.operators["n"]
        u = self.operators["u"]
	# set the matrix elements different from zero to the right values
	# TODO: missing s_p, s_m
        c_up[0,2] = 1.0
        c_up[1,3] = 1.0
        c_up_dag[2,0] = 1.0
        c_up_dag[3,1] = 1.0
        c_down[0,1] = 1.0
        c_down[2,3] = 1.0
        c_down_dag[1,0] = 1.0
        c_down_dag[3,2] = 1.0
        s_z[1,1] = -1.0
        s_z[2,2] = 1.0
        n_up[2,2] = 1.0
        n_up[3,3] = 1.0
        n_down[1,1] = 1.0
        n_down[3,3] = 1.0
        n[1,1] = 1.0
        n[2,2] = 1.0
        n[3,3] = 2.0
        u[3,3] = 1.0
