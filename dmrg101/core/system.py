# 
# File: block.py
# Author: Ivan Gonzalez
#
""" A module for a DMRG system.
"""
from block import make_block_from_site
from dmrg_exceptions import DMRGException
import lanczos 
from make_tensor import make_tensor 
from operators import CompositeOperator 

class System(object):
    """The system class for the DMRG algorithm.

    The system has two blocks, and two single sites, and is the basic
    structure you run the algorithm on. Its main function is to put all
    these things together to avoid having to pass to every time details
    about the underlying chain structure.

    You use this class as a convenience class.

    Examples
    --------
    >>> from dmrg101.core.sites import SpinOneHalfSite
    >>> from dmrg101.core.system import System
    >>> # build a system with four spins one-half.
    >>> spin_one_half_site = SpinOneHalfSite()
    >>> ising_fm_in_field = System(spin_one_half_site)
    >>> # use four strings to name each operator in term
    >>> ising_fm_in_field.add_to_hamiltonian('s_z', 's_z', 'id', 'id')
    >>> ising_fm_in_field.add_to_hamiltonian('id', 's_z', 's_z', 'id')
    >>> ising_fm_in_field.add_to_hamiltonian('id', 'id', 's_z', 's_z')
    >>> # use argument names to save extra typing for some terms
    >>> h = 0.1
    >>> ising_fm_in_field.add_to_hamiltonian(left_block_op='s_z', param=-h)
    >>> ising_fm_in_field.add_to_hamiltonian(left_site_op='s_z', param=-h)
    >>> ising_fm_in_field.add_to_hamiltonian(right_site_op='s_z', param=-h)
    >>> ising_fm_in_field.add_to_hamiltonian(right_block_op='s_z', param=-h)
    >>> gs_energy, gs_wf = ising_fm_in_field.calculate_ground_state()
    >>> print gs_energy
    -0.35
    >>> print gs_wf.as_matrix
    [[ 0.  0.]
    [[ 0.  1.]
    """
    def __init__(self, left_site, right_site=None, left_block=None, right_block=None):
        """Creates the system with the specified sites.

	Exactly that. If you don't provide all the arguments, the missing
	blocks or sites are created from the `left_site` single site
	argument.

	Parameters
	----------
	left_site : a Site object.
	    The site you want to use as a single site at the left.
	right_site : a Site object (optional).
	    The site you want to use as a single site at the right.
	left_block : a Block object (optional).
	    The block you want to use as a single block at the left.
	right_block : a Block object (optional).
	    The block you want to use as a single block at the right.
	"""
    	super(System, self).__init__()
	self.left_site = left_site

	if right_site is not None:
	    self.right_site = right_site
	else:
	    self.right_site = left_site

	if left_block is not None:
	    self.left_block = left_block
	else:
	    self.left_block = make_block_from_site(left_site)

	if right_block is not None:
	    self.right_block = right_block
	else:
	    self.right_block = make_block_from_site(left_site)

	self.left_dim = self.left_block.dim * self.left_site.dim
	self.right_dim = self.right_block.dim * self.right_site.dim
	self.h = CompositeOperator(self.left_dim, self.right_dim)
	self.operators_to_add_to_block = {}
	# 
	# start growing on the left, which may look as random as start
	# growing on the right, but however the latter will ruin the
	# *whole* thing.
	#
	self.set_growing_side('left')

    def set_growing_side(self, growing_side):
	"""Sets which side, left or right, is growing.

	You use this function to change the side which is growing. You
	should set the growing side every time you want to change the
	direction of the sweeps.

	Parameters
	----------
	growing_side : a string.
	    Which side, left or right, is growing.

	Raises
	------
	DMRGException
	    if the `growing_side` is not 'left' or 'right'.
	"""
	if growing_side not in ('left', 'right'):
	    raise DMRGException("Bad growing side")

	self.growing_side = growing_side
	if self.growing_side == 'left':
	    self.growing_site = self.left_site
	    self.growing_block = self.left_block
	else:
	    self.growing_site = self.right_site
	    self.growing_block = self.right_block

    def add_to_hamiltonian(self, left_block_op='id', left_site_op='id', 
    		           right_site_op='id', right_block_op='id',
			   param=1.0):
	"""Adds a term to the hamiltonian.

	You use this function to add a term to the Hamiltonian of the
	system. This is just a convenience function. 

	Parameters
	----------
	left_block_op : a string (optional).
	    The name of an operator in the left block of the system.
	left_site_op : a string (optional).
	    The name of an operator in the left site of the system.
	right_site_op : a string (optional).
	    The name of an operator in the right site of the system.
	right_block_op : a string (optional).
	    The name of an operator in the right block of the system.
	param : a double/complex (optional).
	    A parameter which multiplies the term.

	Raises
	------
	DMRGException 
	    if any of the operators are not in the corresponding
	    site/block.

	Examples
	--------
        >>> from dmrg101.core.sites import SpinOneHalfSite
        >>> from dmrg101.core.system import System
        >>> # build a system with four spins one-half.
        >>> spin_one_half_site = SpinOneHalfSite()
        >>> ising_fm_in_field = System(spin_one_half_site)
        >>> # use four strings to name each operator in term
        >>> ising_fm_in_field.add_to_hamiltonian('s_z', 's_z', 'id', 'id')
        >>> ising_fm_in_field.add_to_hamiltonian('id', 's_z', 's_z', 'id')
        >>> ising_fm_in_field.add_to_hamiltonian('id', 'id', 's_z', 's_z')
        >>> # use argument names to save extra typing for some terms
        >>> h = 0.1
        >>> ising_fm_in_field.add_to_hamiltonian(left_block_op='s_z', param=-h)
        >>> ising_fm_in_field.add_to_hamiltonian(left_site_op='s_z', param=-h)
        >>> ising_fm_in_field.add_to_hamiltonian(right_site_op='s_z', param=-h)
        >>> ising_fm_in_field.add_to_hamiltonian(right_block_op='s_z', param=-h)
	"""
	left_side_op = make_tensor(self.left_block.operators[left_block_op],
		                   self.left_site.operators[left_site_op])
	right_side_op = make_tensor(self.right_block.operators[right_block_op],
		                    self.right_site.operators[right_site_op])
	self.h.add(left_side_op, right_side_op, param)
	
    def add_to_block_hamiltonian(self, block_op='id', site_op='id', param=1.0):
	"""Adds a term to the hamiltonian.

	You use this function to add a term to the Hamiltonian of the
	system. This is just a convenience function. 

	Parameters
	----------
	left_block_op : a string (optional).
	    The name of an operator in the left block of the system.
	left_site_op : a string (optional).
	    The name of an operator in the left site of the system.
	param : a double/complex (optional).
	    A parameter which multiplies the term.

	Raises
	------
	DMRGException 
	    if any of the operators are not in the corresponding
	    site/block.

	Examples
	--------
        >>> from dmrg101.core.sites import SpinOneHalfSite
        >>> from dmrg101.core.system import System
        >>> # build a system with four spins one-half.
        >>> spin_one_half_site = SpinOneHalfSite()
        >>> ising_fm_in_field = System(spin_one_half_site)
        >>> # add the previous block Hamiltonian...
        >>> ising_fm_in_field.add_to_block_hamiltonian(block_op = 'bh')
	>>> # ... and then add the term coming from eating the current site.
        >>> ising_fm_in_field.add_to_block_hamiltonian('s_z', 's_z')
	"""
	tmp = make_tensor(self.growing_block.operators[block_op],
		                      self.growing_site.operators[site_op])
	self.growing_block.operators['bh'] += param * tmp

    def update_all_operators(self, transformation_matrix):
	"""Updates the operators and puts them in the block.

	You use this function to actually create the operators that are
	going to make the block after a DMRG iteration. 

	Parameters
	----------
	transformation_matrix : a numpy array of ndim = 2.

	Returns
	-------
	result : a Block.
	   A new block
	"""
	updated_operators = {}

    def calculate_ground_state(self, initial_wf=None, min_lanczos_iterations=3, 
		               too_many_iterations=1000, precision=0.000001):
	"""Calculates the ground state of the system Hamiltonian.

	You use this function to calculate the ground state energy and
	wavefunction for the Hamiltonian of the system. The ground state
	is calculated using the Lanczos algorithm. This is again a
	convenience function.
	
        Parameters
        ----------
        initial_wf : a Wavefunction, optional
            The wavefunction that will be used as seed. If None, a random one
    	    if used.
        min_lanczos_iterations : an int, optional.
            The number of iterations before starting the diagonalizations.
        too_many_iterations : a int, optional.
            The maximum number of iterations allowed.
        precision : a double, optional.
            The accepted precision to which the ground state energy is
            considered not improving.
        
        Returns 
        -------
        gs_energy : a double.
            The ground state energy.
        gs_wf : a Wavefunction.
            The ground state wavefunction (normalized.)
	"""
	return lanczos.calculate_ground_state(self.h, initial_wf, 
			                      min_lanczos_iterations, 
		                              too_many_iterations, precision)
