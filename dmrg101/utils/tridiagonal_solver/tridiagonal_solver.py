import numpy as np
from tridiagonal_exceptions import TridiagonalException
from lamRange import *
from inversePower3 import *
from eigenvals3 import *

def tridiagonal_solver(d, e, eigenvectors = True):
    """Calculates the eigenvalues and eigenvectors of a tridiagonal and
    symmetric matrix.

    Parameters
    ----------
    d : a numpy array with ndim = 1.
        The elements of the diagonal of the tridiagonal matrix. 
    e : a numpy array with ndim = 1.
        The off-diagonal elements of the tridiagonal matrix. 
    eigenvectors : a bool (optional).
        Whether you want to calculate the eigenvectors.

    Returns
    -------
    evals : a numpy array with ndim = 1.
        The eigenvalues.
    evecs : a numpy array with ndim = 2.
        The eigenvectors.

    Raises
    ------
    TridiagonalException 
        if `d` and `e` have different sizes.
    """
    if (d.size != e.size):
        raise TridiagonalException("d, and e have different sizes")
    num_evals = d.size
    evals = np.empty(num_evals)
    evecs = np.empty((num_evals, num_evals))

    r = lamRange(d, e, num_evals)
    assert(len(r) == num_evals +1)

    evals = eigenvals3(d, e, num_evals)

    if eigenvectors:
        for i in range(num_evals):
    	    evals[i], evecs[:, i] = inversePower3(d, e, 1.00000001*evals[i])
#
#    An alternative that uses the brakets from lamRange:
#
#    if eigenvectors:
#        for i in range(num_evals):
#            s = (r[i] + r[i+1])/2.0
#    	    evals[i], evecs[:, i] = inversePower3(d, e, s)
#    else:
#	evals = eigenvals3(d, e, num_evals)

    return evals, evecs
