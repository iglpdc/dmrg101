#
# File: diagonalize.py
# Author: Ivan Gonzalez
#
"""Diagonalizes a hermitian/square matrix using numpy
"""
import numpy as np
from dmrg_exceptions import DMRGException

def diagonalize(reduced_density_matrix):
    """Diagonalizes a hermitian or symmetric matrix.
    
    You use this function to diagonalize the reduced density matrix. 
    It just calls the corresponding routine in numpy.
    
    Parameters
    ----------
    reduced_density_matrix : a numpy array with ndim = 2 (a matrix) 
        Should be hermitian (if complex), or symmetric (if real).
    
    Returns
    -------
    eigenvals : a numpy array with ndim = 1.
        The eigenvalues (not ordered) of the reduced density matrix.
        The number of eigenvalues is the size if the matrix.
    eigenvecs : a numpy array with ndim = 1.
        The corresponding eigenvectors. Each column correspond to an
        eigenvector, such as eigenvecs[ : i] corresponds to
        eigenvals[i].
    
    Raises
    ------
    DMRGException 
        if the computation cannot be performed.

    Examples
    --------
    >>> import numpy as np
    >>> from dmrg101.core.reduced_DM import diagonalize
    >>> symmetric_matrix = np.array([[0.8, 0.5],
                                     [0.5, -0.25]])
    >>> evals, evecs = diagonalize(symmetric_matrix)
    >>> print evals
    [-0.45 1.0 ]
    >>> tmp = np.dot(evecs, s)
    >>> evecs_diagonalize_the_matrix = np.dot(tmp, evecs.transpose())
    [[ -0.45  0.0 ]
     [  0.0   1.0 ]]    
    >>> hermitian_matrix = np.array([[0.0, -1.0j],
                                     [1.0j, 0.0]], dtype=complex)
    >>> evals, evecs = diagonalize(hermitian_matrix)
    >>> print evals
    [-1. 1.]
    >>> tmp = np.dot(evecs, s)
    >>> evecs_diagonalize_the_matrix = np.dot(tmp, evecs.transpose())
    [[ -1.0  0.0 ]
     [  0.0  1.0 ]]    
    """
    try:
        eigenvals, eigenvecs = np.linalg.eigh(reduced_density_matrix)	
    except LinAlgError:
	raise DMRGException("Error diagonalizing the reduced DM")

    return (eigenvals, eigenvecs)

def truncate(reduced_density_matrix_eigenvals,
	     reduced_density_matrix_eigenvecs, 
	     number_of_states_to_keep):
    """Truncates both the set of eigenvalues and eigenvectors.
    
    You use this function to truncate the set of eigenvalues and
    eigenvectors of the reduced density matrix to keep only the ones
    with larger eigenvalue. The number of eigenvalues kept is
    number_of_states_to_keep.

    If the number_of_states_to_keep is larger than the number of
    eigenvalues, all the eigenvalues are kept.
    
    The order of the columns in the matrix with the eigenvectors is
    not changed, i.e. if in the reduced_density_matrix passed as
    argument, the eigenvectors for the i-th and j-th eigenvalues
    satisfied i < j and both are kept, then i_p < j_p, where i_p, j_p
    are the column indexes that these eigenvectors occupy in the 
    the resulting truncated matrix.
    
    Parameters
    ----------
    reduced_density_matrix_eigenvals: a numpy array with ndim = 1
        The eigenvalues of the reduced density matrix (not need to be
	ordered).
    reduced_density_matrix_eigenvecs: a numpy array with ndim = 2
        The eigenvectors of the reduced density matrix.
    number_of_states_to_keep: an int 
        The number of eigenvalues (or eigenvectors) kept. It is the same
	as the dimension of the truncated Hilbert space.
    
    Returns
    -------
    truncated_eigenvals: a numpy array with ndim = 1.
        The eigenvalues kept in the same order as before.
    transformation_matrix: a numpy array with ndim = 2.
        The eigenvectors kept. this defines the DMRG transformation (a.k.a.
        truncation) matrix.

    Raises
    ------
    DMRGException 
        if the eigenvalues are not a 1-dim array, or the matrix with the
	eigenvecs is not square and with the proper dimensions.

    Examples
    --------
    >>> import numpy as np
    >>> from dmrg101.core.reduced_DM import diagonalize, truncate
    >>> already_diag = np.array([[ 2.0, 0.0, 0.0 ],
    			         [ 0.0, 1.0, 0.0 ],
    			         [ 0.0, 0.0, 3.0 ]])
    >>> evals, evecs = diagonalize(already_diag)
    >>> truncated_evals, truncation_matrix = truncate(evecs, evals, 2) 
    >>> print truncated_evals
    [ 2. 3.]
    >>> print truncation_matrix
    [[ 1.  0.]
     [ 0.  0.]
     [ 0.  1.]]
    """
    if reduced_density_matrix_eigenvals.ndim != 1:
        raise DMRGException("Bad arg: reduced_density_matrix_eigenvals")
    
    number_of_states = reduced_density_matrix_eigenvals.size

    if reduced_density_matrix_eigenvecs.shape != (number_of_states, 
		                                  number_of_states):
        raise DMRGException("Bad arg: reduced_density_matrix_eigenvecs")
   
    # if you don't have enough states, keep them all
    if (number_of_states_to_keep > number_of_states):
	number_of_states_to_keep = number_of_states
    #
    # sort the *indexes* of the eigenvals array (not the eigenvals themselves)
    # according to their eigenval in increasing order
    #
    indexes_in_increasing_order = np.argsort(reduced_density_matrix_eigenvals)
    #
    # get last number_of_states_to_keep of these indexes, i.e. the ones that
    # correspond to the largest number_of_states_to_keep eigenvals, and
    # reorder them back, so you don't change the original order of 
    # the eigenvalues and eigenvectors. 
    #
    indexes_to_keep = np.sort(
		    indexes_in_increasing_order[-number_of_states_to_keep:])
    # 
    # numpy arrays support fancy indexing, such that given a subset of
    # the indexes to the original array gives a view of the array with
    # only the selected indexes.
    #
    truncated_eigenvals = reduced_density_matrix_eigenvals[indexes_to_keep]
    # 
    # Making a (deep) copy is better, as then the resulting arrays are
    # contiguous in memory, i.e. pickup extra optimizations when
    # used in numerical calculations.
    #
    transformation_matrix = np.copy(
		    reduced_density_matrix_eigenvecs[:, indexes_to_keep])
    #
    # a few checks 
    #
    assert(truncated_eigenvals.size == number_of_states_to_keep)
    assert(transformation_matrix.shape == (number_of_states,
	                                   number_of_states_to_keep))
    return (truncated_eigenvals, transformation_matrix)
