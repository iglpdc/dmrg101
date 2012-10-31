# 
# File: entropies.py
# Author: Ivan Gonzalez
# 
"""Functions to calculate entanglement entropies
"""
from math import log
from sys import float_info
from numpy import vectorize, power

def calculate_xlogx(x, epsilon):
    """Calculates :math:`x\log x` of the argument
    
    This is a little helper for the calculate_entropy function.
    It just does what it says.
    
    Parameters
    ----------
    x : a double
        the argument
    epsilon : a double 
        a cut-off to avoid the log going to minus infty.
    
    Returns
    -------
    result : a double 
        xlog(x) if x > epsilon, otherwise returns 0.0.

    Examples
    --------
    >>> from dmrg101.core.entropies import calculate_xlogx
    >>> from sys import float_info
    >>> eigenval_ok = 0.5
    >>> print calculate_entropy(eigenval_ok, float_info.epsilon)
    -0.34657359028
    >>> eigenval_too_small = 0.0
    >>> print calculate_entropy(eigenval_too_small, float_info.epsilon)
    0.0
    """
    result = 0.0
    if x > epsilon:
        result = x * log(x)
    return result

def calculate_entropy(reduced_density_matrix_evals):
    """Calculates the Von Neumann entanglement entropy
    
    You use this function to calculate the Von Neumann entanglement
    entropy for a given set of reduced density matrix evals. The
    function does not care whether you truncate or not the reduced
    density matrix, it just gives the result for the evals you pass it.
    
    The Von Neumann entanglement entropy is defined as:
    
    .. math::
    	S_{vN}=-\sum_{i}\lambda_{i}ln\lambda{i}

    where :math:`\lambda_{i}` are the eigenvalues of the reduced density matrix.
    
    Parameters
    ----------
    reduced_density_matrix_evals : an numpy array 
        The eigenvalues (or some of them) of the reduced density matrix.
    
    Returns
    -------
    result : a double 
        The value of the entropy

    Examples
    --------
    >>> from dmrg101.core.entropies import calculate_entropy
    >>> import numpy as np
    >>> reduced_DM_evals = np.array([0.5, 0.5])
    >>> s_vN = calculate_entropy(reduced_DM_evals)
    >>> print s_vN
    0.69314718056
    """
    vec_xlogx = vectorize(calculate_xlogx)
    result = -sum(vec_xlogx(reduced_density_matrix_evals,
	                    float_info.epsilon))
    return result

def calculate_renyi(reduced_density_matrix_evals, n=2):
    """Calculates the n-th Renyi entropy

    You use this function to calculate the n-th Renyi entanglement entropy 
    entropy for a given set of reduced density matrix evals. The
    function does not care whether you truncate or not the reduced
    density matrix.
    
    The n-th Renyi entanglement entropy is defined as:
    
    .. math::
    	S_{n}=\\frac{1}{1-n}ln\left(\sum_{i}\lambda^{n}_{i}\\right)

    where :math:`\lambda_{i}` are the eigenvalues of the reduced density matrix.

    The value for n = 1 corresponds to the Von Neumann entanglement
    entropy.
    
    Parameters
    ----------
    reduced_density_matrix_evals : an numpy array 
        The eigenvalues of the reduced density matrix.
    n : an int
        The order of the Renyi entropy.
    
    Returns
    -------
    result : a double 
        The value of the entropy.

    Examples
    --------
    >>> from dmrg101.core.entropies import calculate_renyi
    >>> import numpy as np
    >>> reduced_DM_evals = np.array([0.5, 0.5])
    >>> s_2 = calculate_renyi(reduced_DM_evals)
    >>> print s_2
    0.69314718056
    >>> s_3 = calculate_renyi(reduced_DM_evals, 3)
    >>> print s_3
    0.69314718056
    """
    result = 0.0
    if n == 1:
	result = calculate_entropy(reduced_density_matrix_evals)
    else:
        result = log(sum(power(reduced_density_matrix_evals, n)))
	result /= (1.0-n)
    return result
