# 
# File: block.py
# Author: Ivan Gonzalez
#
""" A module for a DMRG system.
"""
from block import make_block_from_site, Block
from dmrg_exceptions import DMRGException
import lanczos 
from make_tensor import make_tensor 
from operators import CompositeOperator 
from transform_matrix import transform_matrix 
from entropies import calculate_entropy, calculate_renyi
from reduced_DM import diagonalize, truncate
from truncation_error import calculate_truncation_error

def make_updated_block_for_site(transformation_matrix,
		                operators_to_add_to_block):
    """Make a new block for a list of operators.

    Takes a dictionary of operator names and matrices and makes a new
    block inserting in the `operators` block dictionary the result of
    transforming the matrices in the original dictionary accoring to the
    transformation matrix.

    You use this function everytime you want to create a new block by
    transforming the current operators to a truncated basis. 

    Parameters
    ----------
    transformation_matrix : a numpy array of ndim = 2.
        The transformation matrix coming from a (truncated) unitary
	transformation.
    operators_to_add_to_block : a dict of strings and numpy arrays of ndim = 2.
        The list of operators to transform.

    Returns
    -------
    result : a Block.
        A block with the new transformed operators.
    """
    cols_of_transformation_matrix = transformation_matrix.shape[1]
    result = Block(cols_of_transformation_matrix)
    for key in operators_to_add_to_block.keys():
	result.add_operator(key)
	result.operators[key] = transform_matrix(operators_to_add_to_block[key],
			               transformation_matrix)
	# debug only 
	#print operators_to_add_to_block[key]
	#print transformation_matrix
	#print result.operators[key]
	#print '--------'
	# end debug only 
    return result

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

	self.h = CompositeOperator(self.get_left_dim(), self.get_right_dim())
	self.operators_to_add_to_block = {}
	self.old_left_blocks = []
	self.old_right_blocks = []
	# 
	# start growing on the left, which may look as random as start
	# growing on the right, but however the latter will ruin the
	# *whole* thing.
	#
	self.set_growing_side('left')
	self.number_of_sites = None
	self.model = None

    def clear_hamiltonian(self):
        """Makes a brand new hamiltonian.
	"""
	self.h = CompositeOperator(self.get_left_dim(), self.get_right_dim())

    def get_left_dim(self):
	"""Gets the dimension of the Hilbert space of the left block
	"""
	return self.left_block.dim * self.left_site.dim
    
    def get_right_dim(self):
	"""Gets the dimension of the Hilbert space of the right block
	"""
	return self.right_block.dim * self.right_site.dim

    def get_shriking_block_next_step_size(self, left_block_size):
	"""Gets the size of the shrinking block in the next DMRG step.

	Gets the size of the shrinking block, i.e. the number of sites
	(not including the single site), in the next step of the finite
	DMRG algorithm.

	Parameters
	----------
	left_block_size : an int.
	    The *current*, i.e. at the current DMRG step, number of sites
	    of the left block (despite the sweep is to the left or the
	    right.) Again this does not include the single site.

	Returns
	-------
	result : a int.
	   The number of sites of the shrinking block, without including
	   the single site.
	"""
	result = None
	if self.growing_side == 'left':
	    result = self.number_of_sites - (left_block_size + 3)
        else:
	    result = left_block_size - 1
	return result

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
	    self.shrinking_site = self.right_site
	    self.shrinking_block = self.right_block
	    self.shrinking_side = 'right'
	else:
	    self.growing_site = self.right_site
	    self.growing_block = self.right_block
	    self.shrinking_site = self.left_site
	    self.shrinking_block = self.left_block
	    self.shrinking_side = 'left'

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
	
    def add_to_operators_to_update(self, name, block_op='id', site_op='id'):
	"""Adds a term to the hamiltonian.

	You use this function to add an operator to the list of operators
	that you need to update. You need to update an operator if it is
	going to be part of a term in the Hamiltonian in any later step in
	the current sweep.

	Parameters
	----------
	name : a string.
	    The name of the operator you are including in the list to
	    update.
	left_block_op : a string (optional).
	    The name of an operator in the left block of the system.
	left_site_op : a string (optional).
	    The name of an operator in the left site of the system.

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
        >>> # some stuff here..., but the only operator that you need to
	>>> # update is 's_z' for the last site of the block.
        >>> ising_fm_in_field.add_to_operators_to_update(site_op='s_z')
	>>> print ising_fm_in_field.operators_to_add_to_block.keys()
	('s_z')
	"""
	tmp = make_tensor(self.growing_block.operators[block_op],
		                      self.growing_site.operators[site_op])
	self.operators_to_add_to_block[name] = tmp

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
	#assert('bh' in self.growing_block.operators.keys())
	#self.growing_block.operators['bh'] += param * tmp

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
	if self.growing_side == 'left':
	    self.old_left_blocks.append(self.left_block)
	    self.left_block = make_updated_block_for_site(
		    transformation_matrix, self.operators_to_add_to_block)
		    
	else:
	    self.old_right_blocks.append(self.right_block)
	    self.right_block = make_updated_block_for_site(
		    transformation_matrix, self.operators_to_add_to_block)
 
    def set_block_to_old_version(self, left_block_size):
	"""Sets the block for the shriking block to an old version.

	You use this function in the finite version of the DMRG algorithm
	to set an shriking block to an old version.

	Parameters
	----------
	left_block_size : an int.
	    The size (not including the single site) of the left block in
	    the *current* step, despite the sweep be to the left or right.
	"""
	shrinking_size = self.get_shriking_block_next_step_size(left_block_size)
	print left_block_size
	print shrinking_size
	if self.shrinking_side == 'left':
	    self.shrinking_block = self.old_left_blocks[shrinking_size-1]
	else:
	    self.shrinking_block = self.old_right_blocks[shrinking_size-1]

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

    def grow_block_by_one_site(self, growing_block, ground_state_wf, 
    		               number_of_states_kept):
        """Grows one side of the system by one site.
    
        Calculates the truncation matrix by calculating the reduced density
        matrix for `ground_state_wf` by tracing out the degrees of freedom of
        the shrinking side. Then updates the operators you need in the next
        steps, effectively growing the size of the block by one site. 	
        
        Parameters
        ----------
        growing_block : a string.
            The block which is growing. It must be 'left' or 'right'.
        ground_state_wf : a Wavefunction.
            The ground state wavefunction of your system.
        number_of_states_kept : an int.
            The number of states you want to keep in each block after the
    	    truncation. If the `number_of_states_kept` is smaller than the
    	    dimension of the current Hilbert space block, all states are kept.
     
        Returns
        -------
        entropy : a double.
            The Von Neumann entropy for the cut that splits the chain into two
    	    equal halves.
        truncation_error : a double.
            The truncation error, i.e. the sum of the discarded eigenvalues of
    	    the reduced density matrix.
        """
        system.set_growing_side(growing_block)
        rho = ground_state_wf.build_reduced_density_matrix(system.shrinking_side)
        evals, evecs = diagonalize(rho)
        truncated_evals, truncation_matrix = truncate(evals, evecs,
    		                                  number_of_states_kept)
        entropy = calculate_entropy(truncated_evals)
        truncation_error = calculate_truncation_error(truncated_evals)
        self.set_block_hamiltonian()
        self.set_operators_to_update()
        system.update_all_operators(truncation_matrix)
        return entropy, truncation_error

    def set_hamiltonian(self):
        """Sets a system Hamiltonian to the model Hamiltonian.

	Just a wrapper around the corresponding `Model` method.
	"""
	self.model.set_hamiltonian(self)
    
    def set_block_hamiltonian(self):
        """Sets the block Hamiltonian to model block Hamiltonian.
	
	Just a wrapper around the corresponding `Model` method.
	"""
	self.model.set_block_hamiltonian(self)
    
    def set_operators_to_update(self):
        """Sets the operators to update to be what you need to AF Heisenberg.
	
	Just a wrapper around the corresponding `Model` method.
	"""
	self.model.set_operators_to_update(self)

    def infinite_dmrg_step(self, number_of_states_kept):
        """Performs one step of the (asymmetric) infinite DMRG algorithm.
    
        Calculates the ground state of a system with a given size, then
        performs the DMRG transformation on the operators of *one* block,
        therefore increasing by one site the number of sites encoded in the
        Hilbert space of this block, and reset the block in the system to be
        the new, enlarged, truncated ones. The other block is kept one-site
        long.
    
        Parameters
        ----------
        number_of_states_kept : an int.
            The number of states you want to keep in each block after the
    	truncation. If the `number_of_states_kept` is smaller than the
    	dimension of the current Hilbert space block, all states are kept.
     
        Returns
        -------
        energy : a double.
            The energy for the `current_size`.
        entropy : a double.
            The Von Neumann entropy for the cut that splits the chain into two
    	    equal halves.
        truncation_error : a double.
            The truncation error, i.e. the sum of the discarded eigenvalues of
    	    the reduced density matrix.
    
        Notes
        -----
        This asymmetric version of the algorithm when you just grow one of the
        block while keeping the other one-site long, is obviously less precise
        than the symmetric version when you grow both sides. However as we are
        going to sweep next using the finite algorithm we don't care much
        about precision at this stage.
        """
        self.model.set_hamiltonian()
        ground_state_energy, ground_state_wf = self.calculate_ground_state()
        entropy, truncation_error = self.grow_block_by_one_site('left', 
			                                        ground_state_wf, 
    		                                                number_of_states_kept)
        return ground_state_energy, entropy, truncation_error
    
    def finite_dmrg_step(self, growing_block, left_block_size, number_of_states_kept):
        """Performs one step of the finite DMRG algorithm.
    
        Calculates the ground state of a system with a given size, then
        performs the DMRG transformation on the operators of *one* block,
        therefore increasing by one site the number of sites encoded in the
        Hilbert space of this block, and reset the block in the system to be
        the new, enlarged, truncated ones. The other block is read out from
        the previous sweep.
    
        Parameters
        ----------
        growing_block : a string.
            The block which is growing. It must be 'left' or 'right'.
        left_block_size : an int.
            The number of sites in the left block in the *current* step, not
    	    including the single site.     
        number_of_states_kept : an int.
            The number of states you want to keep in each block after the
    	    truncation. If the `number_of_states_kept` is smaller than the
    	    dimension of the current Hilbert space block, all states are kept.
     
        Returns
        -------
        energy : a double.
            The energy at this step.
        entropy : a double.
            The Von Neumann entropy for the cut at this step.
        truncation_error : a double.
            The truncation error, i.e. the sum of the discarded eigenvalues of
    	the reduced density matrix.
    
        Raises
        ------
        DMRGException
            if `growing_side` is not 'left' or 'right'.
    
        Notes
        -----
        This asymmetric version of the algorithm when you just grow one of the
        block while keeping the other one-site long, is obviously less precise
        than the symmetric version when you grow both sides. However as we are
        going to sweep next using the finite algorithm we don't care much
        about precision at this stage.
        """
        self.set_hamiltonian()
        ground_state_energy, ground_state_wf = self.calculate_ground_state()
        if growing_block not in ('left', 'right'):
    	    raise DMRGException('Growing side must be left or right.')
    
        entropy, truncation_error = self.grow_block_by_one_site(growing_block, 
    		                                                ground_state_wf,
    		                                                number_of_states_kept)
        self.set_block_to_old_version(left_block_size)
        return ground_state_energy, entropy, truncation_error
