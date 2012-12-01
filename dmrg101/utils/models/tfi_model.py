"""A few convenience functions to setup the Ising model in a TF.

TFIM stands for Ising model in a transverse field, i.e.:

.. math::
    H=\sum_{i}\left[S^{z}_{i}S^{z}_{i+1} + h S^{x}_{i}\right)\right]
"""
class TranverseFieldIsingModel(object):
    """Implements a few convenience functions for the TFIM.
    
    Does exactly that.
    """
    def __init__(self, h = 0):
        super(TranverseFieldIsingModel, self).__init__()
	self.h = h
		
    def set_hamiltonian(self, system):
        """Sets a system Hamiltonian to the TFIM Hamiltonian.
    
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
        system.add_to_hamiltonian('id', 's_z', 's_z', 'id')
        system.add_to_hamiltonian('s_z', 's_z', 'id', 'id')
        system.add_to_hamiltonian('id', 'id', 'id', 's_x', self.h)
        system.add_to_hamiltonian('id', 'id', 's_x', 'id', self.h)
        system.add_to_hamiltonian('id', 's_x', 'id', 'id', self.h)
        system.add_to_hamiltonian('s_x', 'id', 'id', 'id', self.h)
    
    def set_block_hamiltonian(self, system):
        """Sets the block Hamiltonian to be what you need for TFIM.
    
        Parameters
        ----------
        system : a System.
            The System you want to set the Hamiltonian for.
        """
        # If you have a block hamiltonian in your block, add it
        if 'bh' in system.growing_block.operators.keys():
            system.add_to_block_hamiltonian('bh', 'id')
        system.add_to_block_hamiltonian('s_z', 's_z')
        system.add_to_hamiltonian('id', 's_x', self.h)
        system.add_to_hamiltonian('s_x', 'id', self.h)
    
    def set_operators_to_update(self, system):
        """Sets the operators to update to be what you need to TFIM.
    
        Parameters
        ----------
        system : a System.
            The System you want to set the Hamiltonian for.
        """
        # If you have a block hamiltonian in your block, update it
        if 'bh' in system.growing_block.operators.keys():
            system.add_to_operators_to_update('bh', block_op='bh')
        system.add_to_operators_to_update('s_z', site_op='s_z')
        system.add_to_operators_to_update('s_x', site_op='s_x')
