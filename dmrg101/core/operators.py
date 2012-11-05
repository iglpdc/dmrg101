# 
# File: operators.py
# Author: Ivan Gonzalez
#
"""The classes for quantum mechanical operators. 
"""
import numpy as np
from dmrg101.core.dmrg_exceptions import DMRGException
from dmrg101.core.wavefunction import Wavefunction

class OperatorComponent(object):
    """Abstract class for the composite pattern.
    
    This is an abstract class that just serves as a base for the
    implementation of the composite pattern.
    """
    def __init__(self,  left_dim, right_dim):
        super(object, self).__init__()
        self.left_dim = left_dim
        self.right_dim = right_dim
    
    def apply(self, wf):
        """Abstract method to apply the operator

        Does nothing actually.

        Parameters
        ----------
        wf : a Wavefunction
     	    The wavefunction you want to apply the operator.
        """
        pass

class Operator(OperatorComponent):
    """A class for operators.

    This is the leaf class for the implementation of the composite
    pattern.

    You use this class when you want to build an operator that is not part
    of a linear combination of operators.

    Examples
    --------
    >>> import numpy as np
    >>> from dmrg101.core.operators import Operator
    >>> # let's define the Pauli matrices
    >>> s_z = np.array([[-0.5, 0.0],
    ...                 [0.0, 0.5]])	    
    >>> # hamiltonian of the Ising model for two spins 1/2
    >>> ising = Operator(s_z, s_z)
    >>> print ising.left_dim 
    2
    >>> print ising.right_dim 
    2
    >>> print ising.left_op
    [[-0.5  0. ]
     [ 0.   0.5]]
    >>> print ising.right_op
    [[-0.5  0. ]
     [ 0.   0.5]]
    >>> print ising.parameter
    1.0
    """
    def __init__(self, left_op, right_op, parameter=1.0):
	"""Initalizes the operator.

	Checks the operator you are passing are square matrices.

	Parameters
	----------
	left_op : a numpy array of ndim = 2.
	    The operator acting on the left indexes of the wavefunction.
	right_op : a numpy array of ndim = 2.
	    The operator acting on the right indexes of the wavefunction.
	parameter : a double/complex, optional
	    A parameter that multiplies the whole thing.

	Raises
	------
	DMRGException 
	    if any of the matrices you pass are not square.
	"""
    	super(OperatorComponent, self).__init__()
	if left_op.shape[1] != left_op.shape[0]:
	    raise DMRGException("Left operator is not a square matrix")
	if right_op.shape[1] != right_op.shape[0]:
	    raise DMRGException("Right operator is not a square matrix")
    	self.left_dim = left_op.shape[0]
    	self.right_dim = right_op.shape[0]
        self.left_op = left_op
        self.right_op = right_op
        self.parameter = parameter
    
    def apply(self, wf):
    	"""
    	Applies the operator to a wavefunction.

    	Parameters
    	----------
    	wf : A Wavefunction
    	    The wavefunction you want to apply the operator.
    
    	Returns
    	-------
    	result : a Wavefunction
    	    The wavefunction resulting of the operation. It has the same
	    shape (i.e. is in the same Hilbert space) as the one passed as
	    argument.
    
    	Raises
    	------
    	DMRGException
	    if `wf` is has not the correct dimensions as a matrix.
	
	Examples
	--------
	>>> import numpy as np
	>>> from dmrg101.core.operators import Operator
	>>> from dmrg101.core.wavefunction import Wavefunction
	>>> wf = Wavefunction(2, 2)
	>>> wf.randomize()
	>>> identity_operator = Operator(np.eye(2, 2), np.eye(2, 2))
	>>> new_wf = identity_operator.apply(wf)
	>>> np.array_equal(new_wf.as_matrix,  wf.as_matrix)
	True
    	"""
        if wf.as_matrix.shape != ((self.left_dim, self.right_dim)):
     	    raise DMRGException("Wavefunction does not fit.")
        
        result = Wavefunction(self.left_dim, self.right_dim)

        tmp = np.dot(self.right_op, wf.as_matrix.transpose())
	result.as_matrix = np.dot(self.left_op, tmp.transpose())

	return result
		
class CompositeOperator(OperatorComponent):
    """A class for composite operators.
    
    This is the composite class for the implementation of the composite
    pattern. 

    You use this class when you want to build an operator that it is a
    linear combination of other operators. 

    Examples
    --------
    >>> import numpy as np
    >>> from dmrg101.core.operators import CompositeOperator
    >>> # let's define the Pauli matrices
    >>> s_z = np.array([[-0.5, 0.0],
    ...                 [0.0, 0.5]])	    
    >>> s_x = np.array([[0.0, 1.0],
    ...                 [1.0, 0.0]])	    
    >>> one = np.array([[1.0, 0.0],
    ...                 [0.0, 1.0]])	    
    >>> # hamiltonian of the TFIM for two spins 1/2
    >>> ising_in_tf = CompositeOperator(2, 2)
    >>> ising_in_tf.add(s_z, s_z)
    >>> # this is the magnetic field
    >>> h = 0.5
    >>> ising_in_tf.add(one, s_x, h)
    >>> ising_in_tf.add(s_x, one, h)
    >>> print ising_in_tf.list_of_components # doctest: +ELLIPSIS
    [...

    """
    def __init__(self, left_dim, right_dim):
    	super(OperatorComponent, self).__init__()
    	self.left_dim = left_dim
    	self.right_dim = right_dim
    	self.list_of_components = []
    
    def add(self, left_op, right_op, parameter=1.0):
    	"""
    	Add an operator to the composite.

	Parameters
	----------
	left_op : a numpy array of ndim = 2.
	    The operator acting on the left indexes of the wavefunction.
	right_op : a numpy array of ndim = 2.
	    The operator acting on the right indexes of the wavefunction.
	parameter : a double/complex.
	    A parameter that multiplies the whole thing.
    	"""
	op = Operator(left_op, right_op, parameter)
	if op.left_dim != self.left_dim or op.right_dim != self.right_dim:
	    raise DMRGException("Operator cannot be added to composite")
        self.list_of_components.append(op)
    
    def apply(self, wf):
    	"""
    	Applies the composite operator to a wavefunction.

	Applies each of the operator components that form the composite
	operator and sums up the results.
    
    	Parameters
    	----------
    	wf : A Wavefunction
    	    The wavefunction you want to apply the operator.
    
    	Returns
    	-------
    	result : a Wavefunction
    	    The wavefunction resulting of the operation. It has the same
	    shape (i.e. is in the same Hilbert space) as the one passed as
	    argument.
    
    	Raises
    	------
    	DMRGException
    	    if self.list_of_components is empty.
	
	Examples
	--------
	>>> import numpy as np
	>>> from dmrg101.core.operators import CompositeOperator 
	>>> from dmrg101.core.wavefunction import Wavefunction
	>>> wf = Wavefunction(2, 2)
	>>> wf.randomize()
	>>> identity_operator = CompositeOperator(2, 2)
	>>> identity_operator.add(np.eye(2, 2), np.eye(2, 2))
	>>> new_wf = identity_operator.apply(wf)
	>>> np.array_equal(new_wf.as_matrix,  wf.as_matrix)
	True
    	"""
    	if not self.list_of_components:
     	    raise DMRGException("Composite operator is empty.")
         
        result = Wavefunction(self.left_dim, self.right_dim)
	result.set_to_zero()

    	for component in self.list_of_components:
    	    result.as_matrix += component.apply(wf).as_matrix
	return result
