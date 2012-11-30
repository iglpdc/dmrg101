"""A few convenience function to setup the Heisenberg model.
"""

def set_hamiltonian(system):
    """Sets a system Hamiltonian to the AF Heisenberg Hamiltonian.

    Does exactly this. If the system hamiltonian has some other terms on
    it, there are not touched. So be sure to use this function only in
    newly created `System` objects.

    Parameters
    ----------
    system : a System.
        The System you want to set the Hamiltonain for.
    """
    system.clear_hamiltonian()
    if 'bh' in system.left_block.operators.keys():
        system.add_to_hamiltonian(left_block_op='bh')
    if 'bh' in system.right_block.operators.keys():
        system.add_to_hamiltonian(right_block_op='bh')
    system.add_to_hamiltonian('id', 'id', 's_z', 's_z')
    system.add_to_hamiltonian('id', 'id', 's_p', 's_m', .5)
    system.add_to_hamiltonian('id', 'id', 's_m', 's_p', .5)
    system.add_to_hamiltonian('id', 's_z', 's_z', 'id')
    system.add_to_hamiltonian('id', 's_p', 's_m', 'id', .5)
    system.add_to_hamiltonian('id', 's_m', 's_p', 'id', .5)
    system.add_to_hamiltonian('s_z', 's_z', 'id', 'id')
    system.add_to_hamiltonian('s_p', 's_m', 'id', 'id', .5)
    system.add_to_hamiltonian('s_m', 's_p', 'id', 'id', .5)

def set_block_hamiltonian(system):
    """Sets the block Hamiltonian to be what you need for AF Heisenberg.

    Parameters
    ----------
    system : a System.
        The System you want to set the Hamiltonian for.
    """
    # If you have a block hamiltonian in your block, add it
    if 'bh' in system.growing_block.operators.keys():
        system.add_to_block_hamiltonian('bh', 'id')
    system.add_to_block_hamiltonian('s_z', 's_z')
    system.add_to_block_hamiltonian('s_p', 's_m', .5)
    system.add_to_block_hamiltonian('s_m', 's_p', .5)

def set_operators_to_update(system):
    """Sets the operators to update to be what you need to AF Heisenberg.

    Parameters
    ----------
    system : a System.
        The System you want to set the Hamiltonian for.
    """
    # If you have a block hamiltonian in your block, update it
    if 'bh' in system.growing_block.operators.keys():
        system.add_to_operators_to_update('bh', block_op='bh')
    system.add_to_operators_to_update('s_z', site_op='s_z')
    system.add_to_operators_to_update('s_p', site_op='s_p')
    system.add_to_operators_to_update('s_m', site_op='s_m')
