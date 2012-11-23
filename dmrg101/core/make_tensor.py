"""Makes the tensor product of matrices.
"""
import numpy as np

def make_tensor(small_stride_matrix, large_stride_matrix):
    """Makes the tensor product of two matrices.

    The resulting matrix is made up multiplying the two matrices
    block-wise, such as:

    .. math:: 
        result = 
	\\begin{pmatrix} S * L_{1,1} &  S * L_{1,2} & \cdots & S * L_{1,N} \\
	\cdots \\
        S * L_{N,1} &  S * L_{N,2} & \cdots & S * L_{N,N}\\end{pmatrix} 

    where :math:`S` stands for `small_stride_matrix`, 
    :math:`L` stands for `large_stride_matrix`.

    
    Parameters
    ----------
    small_stride_matrix : a numpy array of ndim = 2.
        The small_stride matrix for building the tensor.
    large_stride_matrix : a numpy array of ndim = 2.
        The large_stride matrix for building the tensor.

    Returns
    -------
    result : a numpy array of ndim = 2.
        The result with sizes which are the multiples of the arguments
	sizes.
    """
    small_stride_rows = small_stride_matrix.shape[0] 
    large_stride_rows = large_stride_matrix.shape[0]
    small_stride_cols = small_stride_matrix.shape[1] 
    large_stride_cols = large_stride_matrix.shape[1]
    cols = small_stride_cols * large_stride_cols
    rows = small_stride_rows * large_stride_rows

    result = np.empty([rows, cols])
    for i in range(large_stride_rows):
	ii = i * small_stride_rows
        for j in range(large_stride_cols):
	    jj = j * small_stride_cols
	    result[ii : ii + small_stride_rows, 
	           jj : jj + small_stride_cols] = (small_stride_matrix *
				                   large_stride_matrix[i, j])

    return result
