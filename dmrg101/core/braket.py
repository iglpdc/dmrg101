#
# File : braket.py
# Author : Ivan Gonzalez
#
"""A module to implement quantum-mechanics brakets.
"""
from numpy import inner, conjugate
from dmrg_exceptions import DMRGException

def braket(bra, ket):
    """Takes a bra and a ket and return their braket.

    You use this function to calculate the quantum mechanical braket, i.e.
    the inner product in the wavefunction Hilbert space of two
    wavefunctions.

    The wavefunction in the bra is hermitian conjugated by the braket
    function.

    Parameters
    ----------
    bra : a Wavefunction 
        the bra part of the braket.
    ket : a Wavefunction 
	the ket part of the braket.

    Returns
    -------
    result : a double/complex depending on the type of the wavefuntions
        the value of the braket.
 
    Raises
    ------
    DMRGException
        if the wavefunction don't belong to the same Hilbert space,
        i.e. they have a different number of elements.

    Examples
    --------
    >>> from dmrg101.core.wavefunction import Wavefunction
    >>> from dmrg101.core.braket import braket
    >>> bra = Wavefunction(2,1)
    >>> bra.randomize()
    >>> ket = Wavefunction(2,1)
    >>> ket.randomize()
    >>> print bra, ket
    >>> print braket(bra, ket)
    """
    # use wf.as_matrix to access the matrix elements of wf
    if bra.as_matrix.shape() != ket.as_matrix.shape():
	raise DMRGException("Wavefunctions are not in the same Hilbert space")

    hermitian_conjugated_bra=conjugate(bra.as_matrix).transpose()
    result = inner(hermitian_conjugated_bra, ket.as_matrix)
    return result
