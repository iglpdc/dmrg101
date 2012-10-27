'''
File: truncation_error.py
Author: Ivan Gonzalez
Description: A function to calculate the truncation error
'''
def calculate_truncation_error(reduced_density_matrix_evals):
    """Calculates the DMRG truncation error
    
    In DMRG the truncation error is defined as the sum of the
    eigenvalues whose eigenvectors are left out of the Hilbert space
    in the truncation procedure, that is:
    
    .. math::
    	
    	\epsilon = 1 - \sum_{i}\lambda_{i}
    
    where :math:`lambda_{i}` are the eigenvalues of the density matrix
    that are kept.
    
    Parameters
    ----------
        reduced_density_matrix_evals: a numpy array with the
            reduced density matrix eigenvalues *kept*.
    
    Returns
    -------
        a double with the truncation error
    """
    return 1.0-sum(reduced_density_matrix_evals)
