'''
File: diagonalize.py
Author: Ivan Gonzalez
Description: Diagonalizes a hermitian/square matrix using numpy
'''
import numpy as np
from dmrg_exceptions import DMRGException

def diagonalize(reduced_density_matrix):
    """Diagonalizes a hermitian or square matrix.
    
    You use this function to diagonalize the reduced density matrix. 
    It just calls the corresponding routine in numpy.
    
    Parameters
    ----------
       reduced_density_matrix: a numpy matrix which is hermitian (if
                               complex), or square (if real).
    
    Returns
    -------
       eigenvals: a numpy array with the eigenvalues (not ordered).
                  The number of eigenvalues is the size if the matrix.
       eigenvecs: a numpy array with the corresponding eigenvectors.
       	          Each column correspond to an eigenvector, such as
    	          eigenvecs[ : i] corresponds to eigenvals[i].
    
    Raises
    ______
        DMRGException: if the computation cannot be performed.
    """
    try:
        eigenvals, eigenvecs = np.linalg.eigh(reduced_density_matrix)	
    except LinAlgError:
	raise DMRGException("Error diagonalizing the reduced DM")

    return (eigenvals, eigenvecs)

def truncate(number_of_states_to_keep,
	     reduced_density_matrix_eigenvals,
	     reduced_density_matrix_eigenvecs):
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
        number_of_states_to_keep: an int with the number of eigenvalues (or
                                  eigenvectors) kept. It is the same as 
    			          the dimension of the truncated Hilbert space.
        reduced_density_matrix_eigenvals: a numpy array with the
                                          eigenvalues if the reduced
    				      density matrix (not need to
    				      be ordered).
        reduced_density_matrix_eigenvecs: a numpy array with the
                                          eigenvectors if the reduced
    				      density matrix.
    
    Returns
    -------
        truncated_eigenvals: a numpy array with the eigenvalues kept.
        transformation_matrix: a numpy array with the eigenvectors
                               kept. this defines the DMRG
    			   transformation matrix.
    Raises
    ------
        DMRGException if the eigenvalues are not a 1-dim array, or the
	    matrix with the eigenvecs is not square and with the proper
	    dimensions
    """
    if (reduced_density_matrix_eigenvals.ndim != 1):
        raise DMRGException("Bad arg: reduced_density_matrix_eigenvals")
    
    number_of_states = reduced_density_matrix_eigenvals.size

    if (reduced_density_matrix_eigenvecs.shape != (number_of_states,
      		                                   number_of_states) )
        raise DMRGException("Bad arg: reduced_density_matrix_eigenvecs")
   
    # if you don't have enough states, keep them all
    if (number_of_states_to_keep > number_of_states):
	number_of_states_to_keep = number_of_states
    #
    # sort the indexes of the eigenvals array according to their
    # eigenvalue in increasing order
    #
    indexes_in_increasing_order = np.argsort(reduced_density_matrix_eigenvals)
    #
    # get last number_of_states_to_keep of them, i.e. the ones that
    # correspond to the largest number_of_states_to_keep eigenvals, and
    # reorder them indexes back, so you don't change the original order of 
    # the eigenvalues and eigenvectors. 
    #
    indexes_to_keep = np.sort(indexes_in_increasing_order[-number_of_states_to_keep])
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
    transformation_matrix = copy(reduced_density_matrix_eigenvecs[indexes_to_keep])
    #
    # a few checks 
    #
    assert(truncated_eigenvals.size == number_of_states_to_keep)
    assert(truncated_eigenvals.shape == (number_of_states_to_keep,
	                                 number_of_states_to_keep) )
    return (truncated_eigenvals, transformation_matrix)
