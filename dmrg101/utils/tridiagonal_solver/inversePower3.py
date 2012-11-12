# 
# File: tridiagonal_exceptions.py
# Author: Ivan Gonzalez
# 
"""Inverse power method applied to a tridiagonal matrix.

Adapted from Jaan Kiusalaas, Numerical Methods in Engineering with Python.
"""
import numpy as np
from LUdecomp3 import *
from tridiagonal_exceptions import TridiagonalException

def inversePower3(d, c, s, tol=1.0e-6, max_iterations=100):
    """ Inverse power method for triagonal matrix.

    Inverse power method applied to a tridiagonal matrix
    [A] = [c\d\c]. Returns the eigenvalue closest to 's'
    and the corresponding eigenvector.

    Parameters
    ----------
    d : a numpy array of ndim = 1.
        The matrix in the diagonal.
    c : a numpy array of ndim = 1.
        The matrix in the second-diagonal.
    s : a double.
        The eigenvalue you want to find its eigenvector. This is an
	approximate value.
    tol : a double (optional).
        The overlap between consecutive solutions has to be smaller than
	that to call the eigenvector converged.
    max_iterations : an int.
        The maximum number of iteration done before raising an exception.

    Returns
    -------
    s : a double.
        The eigenvalue corrected.
    x : a numpy array of ndim = 1. 
        The corresponding eigenvector.

    Raises
    ------
    DMRGException 
        if the number of iterations before converging exceeds
	`max_iterations`.
    """
    n = len(d)
    e = c.copy()
    cc = c.copy()                 # Save original [c]
    dStar = d - s                 # Form [A*] = [A] - s[I]
    LUdecomp3(cc,dStar,e)         # Decompose [A*]
    x = np.random.rand(n)         # Seed [x] with random numbers
    norm = np.linalg.norm(x)      # Normalize [x]
    x /= norm
    is_converged = False
    iteration = 0
    sign = 1.0
    while not is_converged:       # Begin iterations    
	iteration +=1
	if iteration > max_iterations:
	    raise TridiagonalException('Inverse power method did not converge')
        xOld = x.copy()           # Save current [x]
        LUsolve3(cc,dStar,e,x)    # Solve [A*][x] = [xOld]
        norm = np.linalg.norm(x)  # Normalize [x]
        x /= norm
        if np.dot(xOld,x) < 0.0:     # Detect change in sign of [x]
            sign = -1.0
            x = -x
	overlap = np.linalg.norm(xOld - x)
        if overlap < tol:
	    is_converged =True
    s += sign/norm
    return s, x
