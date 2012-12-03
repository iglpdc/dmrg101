"""A few convenience functions to setup the Hubbard model.

.. math::
    H=\sum_{i}\vec{S}_{i}\cdot\vec{S}_{i+1}=
    \sum_{i}\left[S^{z}_{i}S^{z}_{i+1}+
    \frac{1}{2}\left(S^{\dagger}_{i}S^{-}_{i+1}+
    S^{-}_{i}S^{\dagger}_{i+1}\right)\right]

"""
class HubbardModel(object):
    """Implements a few convenience functions for Hubbard model.
    
    Does exactly that.
    """
    def __init__(self):
        super(HubbardModel, self).__init__()
		
    def set_hamiltonian(self, system):
        """Sets a system Hamiltonian to the Hubbard Hamiltonian.
    
        Does exactly this. If the system hamiltonian has some other terms on
        it, there are not touched. So be sure to use this function only in
        newly created `System` objects.
    
        Parameters
        ----------
        system : a System.
            The System you want to set the Hamiltonian for.
        """
        system.clear_hamiltonian()
        if 'bh' in system.left_block.operators.keys():
            system.add_to_hamiltonian(left_block_op='bh')
        if 'bh' in system.right_block.operators.keys():
            system.add_to_hamiltonian(right_block_op='bh')
        system.add_to_hamiltonian('c_up', 'c_up_dag', 'id', 'id', -1.)
        system.add_to_hamiltonian('c_up_dag', 'c_up', 'id', 'id', -1.)
        system.add_to_hamiltonian('c_down', 'c_down_dag', 'id', 'id', -1.)
        system.add_to_hamiltonian('c_down_dag', 'c_down', 'id', 'id', -1.)
        system.add_to_hamiltonian('id', 'c_up', 'c_up_dag', 'id', -1.)
        system.add_to_hamiltonian('id', 'c_up_dag', 'c_up', 'id', -1.)
        system.add_to_hamiltonian('id', 'c_down', 'c_down_dag', 'id', -1.)
        system.add_to_hamiltonian('id', 'c_down_dag', 'c_down', 'id', -1.)
        system.add_to_hamiltonian('id', 'id', 'c_up', 'c_up_dag', -1.)
        system.add_to_hamiltonian('id', 'id', 'c_up_dag', 'c_up', -1.)
        system.add_to_hamiltonian('id', 'id', 'c_down', 'c_down_dag', -1.)
        system.add_to_hamiltonian('id', 'id', 'c_down_dag', 'c_down', -1.)
        system.add_to_hamiltonian('u', 'id', 'id', 'id', self.U)
        system.add_to_hamiltonian('id', 'u', 'id', 'id', self.U)
        system.add_to_hamiltonian('id', 'id', 'u', 'id', self.U)
        system.add_to_hamiltonian('id', 'id', 'id', 'u', self.U)
    
    def set_block_hamiltonian(self, tmp_matrix_for_bh, system):
        """Sets the block Hamiltonian to the Hubbard model block Hamiltonian.
    
        Parameters
        ----------
	tmp_matrix_for_bh : a numpy array of ndim = 2.
	    An auxiliary matrix to keep track of the result.
        system : a System.
            The System you want to set the Hamiltonian for.
        """
        # If you have a block hamiltonian in your block, add it
        if 'bh' in system.growing_block.operators.keys():
            system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'bh', 'id')
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'c_up', 'c_up_dag', -1.)
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'c_up_dag', 'c_up', -1.)
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'c_down', 'c_down_dag', -1.)
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'c_down_dag', 'c_down', -1.)
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'id', 'u', self.U)
        system.add_to_block_hamiltonian(tmp_matrix_for_bh, 'u', 'id', self.U)
    
    def set_operators_to_update(self, system):
        """Sets the operators to update to the ones for the Hubbard model.
    
        Parameters
        ----------
        system : a System.
            The System you want to set the Hamiltonian for.

	Notes
	-----
	The block Hamiltonian, althought needs to be updated, is treated
	separately by the very functions in the `System` class.
        """
        system.add_to_operators_to_update('c_up', site_op='c_up')
        system.add_to_operators_to_update('c_up_dag', site_op='c_up_dag')
        system.add_to_operators_to_downdate('c_down', site_op='c_down')
        system.add_to_operators_to_downdate('c_down_dag', site_op='c_down_dag')
        system.add_to_operators_to_update('u', site_op='u')
