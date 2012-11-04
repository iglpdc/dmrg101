#!/usr/bin/env python
""" Calculates the ground state for the AF Heisenberg for two spins 1/2.

Calculates the ground state energy and wavefunction for the
antiferromagnetic Heisenberg model for a system of two spin one-half. The
calculation of the ground state is done using the Lanczos algorithm.
"""
from dmrg101.core.lanczos import calculate_ground_state
from dmrg101.core.operators import Operator
from dmrg101.core.sites import SpinOneHalfSite

def build_HAF_hamiltonian_for_two_spins(left_spin, right_spin):
    """ Builds the AF Heisenberg Hamiltonian for two spins.

    Parameters
    ----------
        left_spin : a Site
	    The Site must have the s_z, s_p, and s_m operators defined.
        right_spin : a Site
	    The Site must have the s_z, s_p, and s_m operators defined.

    Returns
    -------
        result : an Operator
	    The Hamiltonian of the AF Heisenberg.
 
    Notes
    -----
        This function should raise an exception if the keys for the
	operators are not found in the site, but I'll leave without it
	because it just makes the code more complicated to read.
    """
    result = Operator(left_spin.dim, right_spin.dim)
    result.add(left_spin.operators['s_z'], right_spin.operators['s_z'])
    result.add(left_spin.operators['s_p'], right_spin.operators['s_m'], .5)
    result.add(left_spin.operators['s_m'], right_spin.operators['s_p'], .5)
    return result

def main():
    # 
    # create the two spin one-half sites
    #
    left_spin = SpinOneHalfSite()
    right_spin = SpinOneHalfSite()
    #
    # build the Hamiltonian, and solve it using Lanczos.
    #
    hamiltonian = build_HAF_hamiltonian_for_two_spins(left_spin,
		                                      right_spin)
    ground_state_energy, ground_state_wf = calculate_ground_state(hamiltonian)
    #
    # print results
    #
    print "The ground state energy is %8.6f.", %ground_state_energy
    print "The ground state wavefunction is :",
    print ground_state_wf

if __name__ == '__main__':
    main()
