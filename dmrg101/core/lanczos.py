#
# File: lanczos.py
# Author: Ivan Gonzalez
#
""" Implements the Lanczos algorithm
"""
import numpy as np
from math import fabs
from sys import float_info
from dmrg101.core.braket import braket
from dmrg101.core.dmrg_exceptions import DMRGException
from dmrg101.core.wavefunction import create_empty_like
from dmrg101.core.wavefunction import Wavefunction

def create_lanczos_vectors(initial_wf):
    """Creates the three Lanczos vectors

    The Lanczos vectors are created empty, but with the proper size and
    type.

    Parameters
    ----------
    initial_wf : a Wavefunction.
        The initial wavefunctionserving as seed in the Lanczos algorithm.
    
    Returns
    -------
    result : a tuple of 3 numpy arrays.
        The three Lanczos vectors. They have the same shape and type as
	initial_wf, but full of garbage.
    """
    result = [create_empty_like(initial_wf), 
	      create_empty_like(initial_wf), 
	      create_empty_like(initial_wf)]
    return result

def generate_tridiagonal_matrix(alpha, beta, iteration):
    """Generates the elements of the tridiagonal matrix

    You use this function to reshuffle the alpha and beta to generate the
    diagonal and off-diagonal elements of the tridiagonal matrix.

    Parameters
    ----------
    alpha : a numpy array with ndim = 1.
        The alpha's in the Lanczos algorithm.
    beta : a numpy array with ndim = 1.
        The beta's in the Lanczos algorithm.
    iteration : an int
        The iteration you are, which sets the size of d, e.
    
    Returns
    -------
    d : a numpy array with ndim = 1.
        The elements of the diagonal.
    e : a numpy array with ndim = 1.
        The off-diagonal elements.
    """
    d = np.copy(alpha[:iteration+1])
    e = np.empty_like(d)
    for i in range(d.size-1):
	e[i] = beta[i+1]
    e[d.size-1] = 0.0
    assert(e.size == d.size)
    assert(e.size == iteration+1)
    return d, e

def diagonalize_tridiagonal_matrix(d, e, eigenvectors):
    """Diagonalizes the tridiagonal matrix in the Lanczos.

    Parameters
    ----------
    alpha : a numpy array with ndim = 1.
        The alpha's in the Lanczos algorithm.
    beta : a numpy array with ndim = 1.
        The beta's in the Lanczos algorithm.
  
    Returns
    -------
    evals : a numpy array with ndim = 1.
        The eigenvalues.
    evecs : a numpy array with ndim = 2.
        The eigenvectors.
    """
    return evals, evecs
    
def lanczos_zeroth_iteration(alpha, beta, lv, hamiltonian)
    """Performs the zero-th iteration for the Lanczos.

    The zero-th (i.e. the first at all) Lanczos iteration is slightly
    different to the rest.

    Parameters
    ----------
    alpha : a numpy array with ndim = 1.
        The alpha's in the Lanczos algorithm.
    beta : a numpy array with ndim = 1.
        The beta's in the Lanczos algorithm.
    lv : a 3-tuple of numpy arrays of ndim = 2.
        The Lanczos vectors.
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.
    """
    lv[1] = hamiltonian.apply(lv[0])
    alpha[0] = braket(lv[0], lv[1]) # you will have to deal with real only
    lv[1].as_matrix -= alpha[0]*lv[0].as_matrix
    beta[1] = lv[1].get_norm() 
    lv[1].normalize()

def lanczos_nth_iteration(alpha, beta, lv, hamiltonian, iteration)
    """Performs the zero-th iteration for the Lanczos.

    The zero-th (i.e. the first at all) Lanczos iteration is slightly
    different to the rest.

    Parameters
    ----------
    alpha : a numpy array with ndim = 1.
        The alpha's in the Lanczos algorithm.
    beta : a numpy array with ndim = 1.
        The beta's in the Lanczos algorithm.
    lv : a 3-tuple of numpy arrays of ndim = 2.
        The Lanczos vectors.
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.
    iteration : an int
        The iteration number.
    """
    lv[2] = hamiltonian.apply(lv[1])
    alpha[iter] = braket(lv[1], lv[2])
    lv[2].as_matrix -= (alpha[iteration]*lv[1].as_matrix +
    		    beta[iteration]*lv[0].as_matrix)
    cycle_lanczos_vectors(lv)

def improve_ground_state_energy(d, e, current_gs_energy, precision):
    """Get an improved value for the ground state energy

    Diagonalizes the tridiagonal matrix and find its lowest eigenvalues.
    Then checks whether this lowest eigenvalue imrproves the current
    ground state energy. 

    Parameters
    ----------
    d : a numpy array with ndim = 1.
        The elements of the diagonal of the tridiagonal matrix.
    e : a numpy array with ndim = 1.
        The off-diagonal elements of the tridiagonal matrix.
    current_gs_energy : a double
        The current (best) value for the ground state energy. You use here
	the value coming from the previous iteration of the Lanczos.
    precision : a double.
        The ratio to the current_gs_energy that is accepted as no
	improvement.
    
    Returns
    -------
    does_not_improve_anymore : a bool.
        Whether the new value improves the current one or not.
    new_gs_energy : a double.
        The new value for the ground state energy.
    """
    evals, evecs = diagonalize_tridiagonal_matrix(d, e)
    minimum_eval = min(evals)
    difference_with_current = fabs(gs_energy - minimum_eval)
    acceptable_difference = precision * fabs(gs_energy)
    if (difference_with_current < acceptable_difference):
        does_not_improve_anymore = True
    new_gs_energy = minimum_eval
    return does_not_improve_anymore, new_gs_energy

def calculate_ground_state_energy(hamiltonian, initial_wf,
		                  max_number_iterations, 
				  min_lanczos_iterations, 
				  too_many_iterations,
				  precision):
    """Calculates the ground state energy.

    Parameters
    ----------
    hamiltonian : a CompositeOperator.
        The hamiltonian you want to diagonalize.
    initial_wf : a Wavefunction.
        The wavefunction that will be used as seed. If None, a random one
	if used.
    max_number_iterations : an int.
        The maximum number of iterations before resizing.
    min_lanczos_iterations : an int.
        The maximum number of iterations before starting the
	diagonalizations.
    too_many_iterations : a int.
        The maximum number of iterations before allowed.
    precision : a double.
        The accepted precision to which the ground state energy is
	considered not improving.
    
    Returns
    -------
    gs_energy : a double.
        The ground state energy.
    d : a numpy array with ndim = 1.
        The elements of the diagonal of the tridiagonal matrix.
    e : a numpy array with ndim = 1.
        The off-diagonal elements of the tridiagonal matrix.

    Raises
    ------
    DMRGException 
        if the number of iterations goes over too_many_iterations.
    """
    #TODO which is the type of alpha and beta
    initial_number_of_iterations = max_number_iterations
    alpha = np.array(max_number_iterations)
    beta = np.array(max_number_iterations)
    lv = create_lanczos_vectors(initial_wf)
 
    beta[0] = 0.0 # beta[0] is not defined
    lv[0].as_matrix = np.copy(initial_wf.as_matrix)

    iteration = 0
    lanczos_zeroth_iteration(alpha, beta, lv, hamiltonian)

    # check if the initial_wf is already the ground state
    if beta[1] > float_info.epsilon: # initial_wf is *not* the ground state
        we_are_done = False
        while not we_are_done:
            iteration++
    	    lanczos_nth_iteration(alpha, beta, lv, hamiltonian, iteration)
    
    	    if iteration >= min_lanczos_iterations:
		d, e = generate_tridiagonal_matrix(alpha, beta, iteration)
		we_are_done, gs_energy = improve_ground_state_energy(d, e,
				precision, gs_energy)
    
    	    if not we_are_done and iteration == max_lanczos_iterations-2:
    	        if max_number_iterations >= too_many_iterations:
    	    	    raise DMRGException("Too many Lanczos iterations")
    	        # TODO log this as a warning
    	        max_lanczos_iterations += initial_number_of_iterations
    	        alpha.resize(max_lanczos_iterations)
    	        beta.resize(max_lanczos_iterations)
     else: # initial_wf *is* the ground state
	 gs_energy = alpha[0]
 
    return gs_energy, d, e

def calculate_ground_state(hamiltonian, initial_wf = None, 
		           max_number_iterations = 100, 
			   min_lanczos_iterations = 3, 
		           too_many_iterations = 1000, 
			   precision = 0.0000001):
    """Calculates the ground state energy and wavefunction.

    Parameters
    ----------
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.
    initial_wf : a Wavefunction, optional
        The wavefunction that will be used as seed. If None, a random one
	if used.
    max_number_iterations : an int, optional
        The maximum number of iterations before resizing.
    min_lanczos_iterations : an int, optional.
        The maximum number of iterations before starting the
	diagonalizations.
    too_many_iterations : a int, optional.
        The maximum number of iterations before allowed.
    precision : a double, optional.
        The accepted precision to which the ground state energy is
	considered not improving.
    
    Returns 
    -------
    gs_energy : a double.
        The ground state energy.
    gs_wf : a Wavefunction.
        The ground state wavefunction.
    """
    if initial_wf is None:
        initial_wf = Wavefunction(hamiltonian.left_dim,
			          hamiltonian.right_dim)
	initial_wf.randomize()

    gs_energy, d, e = calculate_ground_state_energy(hamiltonian, initial_wf, 
		                                    max_number_iterations, 
		                                    min_lanczos_iterations, 
		                                    too_many_iterations, 
						    precision)
    gs_wf = calculate_ground_state_wf(d, e)

    return gs_energy, gs_wf
