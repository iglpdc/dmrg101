# 
# File: transform_matrix.py
# Author: Ivan Gonzalez
#
""" A function to transform a matrix to a new (truncated) basis.
"""
import numpy as np
from dmrg_exceptions import DMRGException

def transform_matrix(matrix_to_transform, transformation_matrix):
    """Transforms a matrix to a new (truncated) basis.

    You use this function to perform a change of basis for a given matrix.
    If the transformation matrix is square, it should be unitary.
    Otherwise, it was an unitary matrix with some columns removed (i.e.
    truncated.) Therefore the transformation matrix has always at least
    the same number of rows than columns.

    Parameters
    ----------
    matrix_to_transform : a numpy array of ndim = 2.
        The matrix you want to transform.
    transform_matrix : a numpy array of ndim = 2.
        The transformation matrix.

    Returns
    -------
    result : a numpy array of ndim = 2.
        The matrix transformed to the new (truncated) basis.

    Raises
    ------
    DMRGException
        if `original_matrix` is not square, or `transformation_matrix`
	don't fit `original_matrix`.

    Examples
    --------
    >>> import numpy as np
    >>> from dmrg101.core.reduced_DM import diagonalize
    >>> from dmrg101.core.transform_matrix import transform_matrix
    >>> original_matrix = np.eye(2)
    >>> # get a unitary matrix by diagonalizing a symmetric matrix
    >>> symmetric_matrix = np.array([[0.8, 0.5],
    ...                              [0.5, -0.25]])
    >>> evals, evecs = diagonalize(symmetric_matrix)
    >>> transformed_matrix = transform_matrix(original_matrix, evecs)
    >>> print transformed_matrix
    [[ 1.  0.]
     [ 0.  1.]] 
    """
    if matrix_to_transform.shape[0] != matrix_to_transform.shape[1]:
	raise DMRGException("Cannot transform a non-square matrix")
    if matrix_to_transform.shape[0] != transformation_matrix.shape[0]:
	raise DMRGException("Matrix and transformation don't fit")
    tmp = np.dot(matrix_to_transform, transformation_matrix)
    return np.dot(np.conj(transformation_matrix.transpose()), tmp)
