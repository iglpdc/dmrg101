'''
File: sites.py
Author: Ivan Gonzalez
Description: The class for single sites
'''
from core.exceptions import DMRGException
from numpy import zeros, eye

class Site(object):
    """A general single site
    
    You use this class to create a single site. The site comes empty,
    and you should add operators.
    
    Attributes: 
        dim: An integer with the size of the Hilbert space
        operators: A dictionary with the operators for the site
    """
    def __init__(self, dim):
    	"""Creates an empty site of dimension dim
    
    	The dimension must be at least 1. A site of dim=1 represents the 
	vaccum.

	Raises: 
	    DMRGException: if dim < 1.

	Postcond:
	    The identity operator (ones in the diagonal, zeros elsewhere)
	    is added to the self.operators dictionary.
    	"""
    	if dim < 1:
    		raise DMRGException("Site dim msut be at least 1")
    	super(Site, self).__init__()
    	self.dim = dim
	self.operators={ "id" : eye(self.dim, self.dim) }
    
    def add_operator(self, operator_name):
    	"""Adds an operator to the site
    
    	Attributes:
    	    operator_name: a string with the operator name.

	Raises:
	    DMRGException: if operator_name is already in the dict.
    
    	Postcond:
    	    o self.operators has one item more, and
   	    o the newly created operator is a square matrix of
    	      self.dim times self.dim full of zeros.
            """
	if str(operator_name) in self.operators.keys():
    	    raise DMRGException("Operator name exists already")
    	else:
    	    self.operators[str(operator_name)]=zeros(self.dim, self.dim)


class SpinOneHalfSite(Site):
    """A site for spin 1/2 models
    
    You use this site for models where the single sites are spin
    one-half sites. The Hilbert space is ordered such as the first state
    is the spin down, and the second state is the spin up. Therefore e.g.
    you have the following relation between operator matrix elements:

    .. math:
        \langle \down_arrow| A | \up_arrow\rangle=A_{0,1}
    
    Postcond: 
        The site has already built-in the spin operators for s_z, s_p,
	s_m.
    """
    def __init__(self):
        super(SpinOneHalfSite, self).__init__(2)
	# add the operators
        super(SpinOneHalfSite, self).operators.add["s_z"]
        super(SpinOneHalfSite, self).operators.add["s_p"]
        super(SpinOneHalfSite, self).operators.add["s_m"]
	# set the matrix elements different from zero to the right values
        self.operators["s_z"](0,0)=-1.0
        self.operators["s_z"](1,1)=1.0
        self.operators["s_p"](1,0)=1.0
        self.operators["s_m"](0,1)=1.0


class ElectronicSite(Site):
    """A site for electronic models
    
    You use this site for models where the single sites are electron
    sites. The Hilbert space is ordered such as:
        - the first state, labelled 0,  is the empty site,
	- the second, labelled 1, is spin down, 
	- the third, labelled 2, is spin up, and 
	- the fourth, labelled 3, is double occupancy.
    
    Postcond: 
	The site has already built-in the spin operators for: 
	    - c_up, destroys an spin up electron
	    - c_up_dag, creates an spin up electron
	    - c_down, destroys an spin down electron
	    - c_down_dag, creates an spin down electron
	    - s_z, component z of spin
	    - s_p, raises the component z of spin
	    - s_m, lowers the component z of spin
	    - n_up, number of electrons with spin up
	    - n_down, number of electrons with spin down
	    - n, number of electrons, i.e. n_up+n_down
	    - u, number of double occupancies, i.e. n_up*n_down
    """
    def __init__(self):
        super(ElectronicSiteSpinOneHalfSite, self).__init__(4)
	# add the operators
        super(ElectronicSite, self).operators.add["c_up"]
        super(ElectronicSite, self).operators.add["c_up_dag"]
        super(ElectronicSite, self).operators.add["c_down"]
        super(ElectronicSite, self).operators.add["c_down_dag"]
        super(ElectronicSite, self).operators.add["s_z"]
        super(ElectronicSite, self).operators.add["s_p"]
        super(ElectronicSite, self).operators.add["s_m"]
        super(ElectronicSite, self).operators.add["n_up"]
        super(ElectronicSite, self).operators.add["n_down"]
        super(ElectronicSite, self).operators.add["n"]
        super(ElectronicSite, self).operators.add["u"]
	# set the matrix elements different from zero to the right values
        self.operators["c_up"](0,2)=1.0
        self.operators["c_up"](1,3)=1.0
        self.operators["c_up_dag"](2,0)=1.0
        self.operators["c_up_dag"](3,1)=1.0
        self.operators["c_down"](0,1)=1.0
        self.operators["c_down"](2,3)=1.0
        self.operators["c_down_dag"](1,0)=1.0
        self.operators["c_down_dag"](3,2)=1.0
        self.operators["s_z"](1,1)=-1.0
        self.operators["s_z"](2,2)=1.0
	# todo: missing s_p, s_m
        self.operators["n_up"](2,2)=1.0
        self.operators["n_up"](3,3)=1.0
        self.operators["n_down"](1,1)=1.0
        self.operators["n_down"](3,3)=1.0
        self.operators["n"](1,1)=1.0
        self.operators["n"](2,2)=1.0
        self.operators["n"](3,3)=2.0
        self.operators["u"](3,3)=1.0
