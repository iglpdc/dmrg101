#
# File: lanczos.py
# Author: Ivan Gonzalez
#
""" Implements the Lanczos algorithm.

Implements the Lanczos algorithm to calculate the ground state energy and
wavefunction of a given Hamiltonian. The objects representing the
wavefunction and hamiltonian are Wavefunction and OperatorComponent (i.e.
an Operator or a CompositeOperator), respectively.

Most of the methods here are just convenience functions. The one that
implements the algorithm is :func:`calculate_ground_state`.

Methods
-------

- calculate_ground_state_energy(hamiltonian, initial_wf,
  min_lanczos_iterations, too_many_iterations, precision) : Calculates the
  ground state energy.
- calculate_ground_state_wf(hamiltonian, initial_wf,
- calculate_ground_state(hamiltonian, [initial_wf, min_lanczos_iterations,
  too_many_iterations, precision]): Calculates the ground state energy and
  wavefunction.
- create_lanczos_vectors(initial_wf) : Creates the three Lanczos vectors.
- cycle_lanczos_vectors(lv, saved_lanczos_vectors) : Cycles the Lanczos
  vectors to prepare them for the next iteration.
- diagonalize_tridiagonal_matrix(d, e, eigenvectors) : Diagonalizes the
  tridiagonal matrix in the Lanczos.
- improve_ground_state_energy(d, e, current_gs_energy, precision) : Gets
  an improved value for the ground state energy.
- generate_tridiagonal_matrix(alpha, beta, iteration) : Generates the
  elements of the tridiagonal matrix.
- lanczos_zeroth_iteration(alpha, beta, lv, hamiltonian) : Performs the
  zero-th iteration for the Lanczos.
- lanczos_nth_iteration(alpha, beta, lv, saved_lanczos_vectors,
  hamiltonian, iteration) : Performs the n-th iteration for the Lanczos.

Examples
--------
>>> import numpy as np
>>> from dmrg101.core.operators import CompositeOperator
>>> from dmrg101.core.lanczos import calculate_ground_state
>>> s_z = np.array([[-0.5, 0.0],
...                 [0.0, 0.5]])	    
>>> one = np.array([[1.0, 0.0],
...                 [0.0, 1.0]])	    
>>> ising_fm_in_field = CompositeOperator(2, 2)
>>> ising_fm_in_field.add(s_z, s_z, -1.0)
>>> h = 0.1
>>> ising_fm_in_field.add(s_z, one, -h)
>>> ising_fm_in_field.add(one, s_z, -h)
>>> gs_energy, gs_wf = calculate_ground_state(ising_fm_in_field)
>>> print gs_energy
-0.27
>>> print gs_wf 
[[ 0.  0.]
[[ 0.  1.]

------------------------------------------------------

.. [1] http://en.wikipedia.org/wiki/Lanczos_algorithm
"""
import numpy as np
from math import fabs
from sys import float_info
from dmrg101.core.braket import braket
from dmrg101.core.dmrg_exceptions import DMRGException
from dmrg101.core.get_real import get_real 
from dmrg101.core.wavefunction import create_empty_like
from dmrg101.core.wavefunction import Wavefunction

def create_lanczos_vectors(initial_wf):
    """Creates the three Lanczos vectors.

    The Lanczos vectors are created empty, but with the proper size and
    type. The first lanczos vector is set to have the same eleements as 
    the `initial_wf`.

    Parameters
    ----------
    initial_wf : a Wavefunction.
        The initial wavefunction serving as seed in the Lanczos algorithm.
    
    Returns
    -------
    result : a tuple of 3 numpy arrays.
        The three Lanczos vectors. They have the same shape and type as
	initial_wf. The first has the same elements (is a copy), and the
	last two are full of garbage.
    """
    result = [create_empty_like(initial_wf), 
	      create_empty_like(initial_wf), 
	      create_empty_like(initial_wf)]
    result[0].as_matrix = np.copy(initial_wf.as_matrix)
    return result

def generate_tridiagonal_matrix(alpha, beta, iteration):
    """Generates the elements of the tridiagonal matrix.

    You use this function to reshuffle the alpha and beta to generate the
    diagonal and off-diagonal elements of the tridiagonal matrix. Note
    that `d`, `e` sizes depend on the `iteration`.

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
        The elements of the diagonal of the tridiagonal matrix. The size
	of `d` is `iteration`+1.
    e : a numpy array with ndim = 1.
        The off-diagonal elements of the tridiagonal matrix. The size of
	`d` is `iteration`+1.
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
    #TODO: the real code.
    return evals, evecs
    
def lanczos_zeroth_iteration(alpha, beta, lv, hamiltonian):
    """Performs the zero-th iteration for the Lanczos.

    The zero-th (i.e. the first at all) Lanczos iteration is slightly
    different to the rest.

    Parameters
    ----------
    alpha : a list of doubles.
        The alpha's in the Lanczos algorithm.
    beta :  a list of doubles.
        The beta's in the Lanczos algorithm.
    lv : a 3-tuple of numpy arrays of ndim = 2.
        The Lanczos vectors.
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.

    Returns
    -------
    already_the_ground_state : a bool
        Whether the zeroth iteration gives you the ground state. This
	happens when the initial wavefunction for the Lanczos is already
	the groudn state.
    
    Raises
    ------
    DMRGException :
        if the `alpha` or `beta` lists are not empty.
    """
    if alpha and beta:
        raise DMRGException("Lists not empty at zeroth Lanczos iter")
    beta.append(0.0) # beta[0] is not defined
    lv[1] = hamiltonian.apply(lv[0])
    alpha.append(get_real(braket(lv[0], lv[1])))
    lv[1].as_matrix -= alpha[0]*lv[0].as_matrix
    beta.append(lv[1].get_norm())
    lv[1].normalize()
    assert(len(alpha) == 1)
    assert(len(beta) == 2)
    already_the_ground_state = beta[1] < float_info.epsilon
    return already_the_ground_state

def lanczos_nth_iteration(alpha, beta, lv, saved_lanczos_vectors,
		          hamiltonian, iteration):
    """Performs the n-th iteration for the Lanczos.

    It calculates the new values for `alpha` and `beta` for this
    `iteration`.

    Parameters
    ----------
    alpha : a numpy array with ndim = 1.
        The alpha's in the Lanczos algorithm.
    beta : a numpy array with ndim = 1.
        The beta's in the Lanczos algorithm.
    lv : the 3 tuple of Wavefunctions.
        With the three Lanczos vectors in use.
    saved_lanczos_vectors : a list of Wavefunctions.
        The Lanczos vectors that are saved.
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.
    iteration : an int
        The iteration number.

    Notes
    -----
    Postcond : The 3rd Lanczos vector in the tuple is modified. The first
    two are *not*.
    """
    lv[2] = hamiltonian.apply(lv[1])
    alpha.append(get_real(braket(lv[1], lv[2])))
    lv[2].as_matrix -= (alpha[iteration]*lv[1].as_matrix +
    		        beta[iteration]*lv[0].as_matrix)
    beta.append(lv[2].get_norm())
    lv[2].normalize()
    cycle_lanczos_vectors(lv, saved_lanczos_vectors)
    assert(len(alpha) == iteration + 1)
    assert(len(beta) == iteration + 2)

def cycle_lanczos_vectors(lv, saved_lanczos_vectors):
    """Cycles the Lanczos vectors to prepare them for the next iteration.

    You use this function to cycle the Lanczos vectors in this way:
    - lv[1] -> lv[0]
    - lv[2] -> lv[1]

    The first Lanczos vector before the cycle, `lv[0]` is not needed
    anymore and is appended to the `saved_lanczos_vectors` list. The last
    Lanczos vector after the cycle, `lv[2]` contains garbage.

    Parameters
    ----------
    lv : the 3 tuple of Wavefunctions.
        With the three Lanczos vectors in use.
    saved_lanczos_vectors : a list of Wavefunctions.
        The Lanczos vectors that are saved.
    """
    saved_lanczos_vectors.append(lv[0])
    lv[0], lv[1], lv[2] = lv[1], lv[2], create_empty_like(lv[2])

def improve_ground_state_energy(d, e, current_gs_energy, precision):
    """Gets an improved value for the ground state energy.

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
    if current_gs_energy is not None:
        difference_with_current = fabs(current_gs_energy - minimum_eval)
        acceptable_difference = precision * fabs(current_gs_energy)
        does_not_improve_anymore = (difference_with_current < acceptable_difference)
    else:
	does_not_improve_anymore = False
    new_gs_energy = minimum_eval
    return does_not_improve_anymore, new_gs_energy

def calculate_ground_state_energy(hamiltonian, initial_wf,
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
    min_lanczos_iterations : an int.
        The number of iterations before starting the diagonalizations.
    too_many_iterations : a int.
        The maximum number of iterations allowed.
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
        if the number of iterations goes over `too_many_iterations`.
    """
    alpha = []
    beta = []
    lv = create_lanczos_vectors(initial_wf)
    saved_lanczos_vectors = []
 
    iteration = 0
    is_initial_wf_the_gs = lanczos_zeroth_iteration(alpha, beta, lv, hamiltonian)
    gs_energy = None

    # check if the initial_wf is already the ground state
    if not is_initial_wf_the_gs:
        we_are_done = False
        while not we_are_done:
            iteration += 1
    	    if iteration >= too_many_iterations:
    	    	raise DMRGException("Too many Lanczos iterations")

    	    lanczos_nth_iteration(alpha, beta, lv, saved_lanczos_vectors, 
			          hamiltonian, iteration)

    	    if iteration >= min_lanczos_iterations:
		d, e = generate_tridiagonal_matrix(alpha, beta, iteration)
		we_are_done, gs_energy = improve_ground_state_energy(d, e,
				gs_energy, precision)
    
	assert(we_are_done)
	saved_lanczos_vectors.append(lv[1])
	saved_lanczos_vectors.append(lv[2])
    else: # initial_wf *is* the ground state
	gs_energy = alpha[0]
  
    assert(gs_energy is not None)
    return gs_energy, d, e, saved_lanczos_vectors

def calculate_ground_state(hamiltonian, initial_wf = None, 
			   min_lanczos_iterations = 3, 
		           too_many_iterations = 1000, 
			   precision = 0.000001):
    """Calculates the ground state energy and wavefunction.

    Parameters
    ----------
    hamiltonian : a CompositeOperator
        The hamiltonian you want to diagonalize.
    initial_wf : a Wavefunction, optional
        The wavefunction that will be used as seed. If None, a random one
	if used.
    min_lanczos_iterations : an int, optional.
        The number of iterations before starting the diagonalizations.
    too_many_iterations : a int, optional.
        The maximum number of iterations allowed.
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

    gs_energy, d, e, saved_lanczos_vectors = (
        calculate_ground_state_energy(hamiltonian, initial_wf, min_lanczos_iterations, 
		                      too_many_iterations, precision) )
    gs_wf = calculate_ground_state_wf(d, e, saved_lanczos_vectors)

    return gs_energy, gs_wf
