#
# File: lanczos.py
# Author: Ivan Gonzalez
#
""" Implements the Lanczos algorithm
"""
from dmrg101.core.wavefunction import Wavefunction

def calculate_ground_state(hamiltonian, initial_wf = None):
    """Calculates the ground state energy and wavefunction.

    This is just a mockup right now.
    """
    if initial_wf is None:
        initial_wf = Wavefunction(hamiltonian.left_dim,
			          hamiltonian.right_dim)
	initial_wf.randomize()

    # TODO write the real code here.
    gs_energy = 0.0
    gs_wf = initial_wf

    return gs_energy, gs_wf
