'''
File: braket.py
Author: Ivan Gonzalez
Description: A function to implement quantum-mechanics brakets
'''
from numpy import inner, conjugate
from dmrg_exceptions import DMRGException

def braket(bra, ket):
    """Takes a bra and a ket and return their braket

    You use this function to calculate the quantum mechanical braket, i.e.
    the inner product in the wavefunction Hilbert space of two
    wavefunction.

    The wavefunction in the bra is hermitian conjugated by the braket
    function.

    Parameters
    ----------
        bra: a Wavefunction with the bra part of the braket.
        ket: a Wavefunction with the ket part of the braket.

    Returns
    -------
        a double/complex with value of the braket.
 
    Raises
    ------
        DMRGException: if the wavefunction don't belong to the same
	    Hilbert space, i.e. they have a different number of elements.
    """
    # use wf.as_matrix to access the matrix elements of wf
    if bra.as_matrix.shape() != ket.as_matrix.shape():
	raise DMRGException("Wavefunctions in braket are not in the same
	    		     Hilbert space")

    hermitian_conjugated_bra=conjugate(bra.as_matrix).transpose()
    return inner(hermitian_conjugated_bra, ket.as_matrix)
