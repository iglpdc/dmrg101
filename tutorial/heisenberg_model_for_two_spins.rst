Heisenberg model for two spins
==============================

The goal of this exercise is to build a Hamiltonian for the two spin
system in the previous exercise, and calculate its ground state. Again the
purpose is just to get you familiar with the code.

The Hamiltonian that we will build is the antiferromagnetic Heisenberg
model, which reads like:

.. math::
    H=\vec{S}_{1}\cdot\vec{S}_{2}=S^{z}_{1}S^{z}_{2}+
    \frac{1}{2}\left(S^{\dagger}_{1}S^{-}_{2}+
    S^{-}_{1}S^{\dagger}_{2}\right)

 
where :math:`\vec{S}_{i}=\vec{\sigma}_{i}/2` are the spin operators,
:math:`\sigma_{i}` are the Pauli matrices, and
:math:`S^{\pm}_{i}=S^{x}_{i}\pm i S^{y}_{i}`.

Exercise
--------

Calculate the ground state (energy and wavefunction) of the
antiferromagentic Heisenberg model for a system of two spins one-half.

Hint
----

Two things. First, remember that the wavefunction in the code is written
as a matrix, where the left (row) indexes correspond to the left system,
i.e. the left spin, and where the right (colum) indexes correspond to the
right system, i.e. the right spin.

Second, once we have build up the Hamiltonian we will use the `Lanczos
algorithm <http://en.wikipedia.org/wiki/Lanczos_algorithm>`_ to get its
ground state. This is a whole beast on his own, and we are not going to
enter much into it. Just believe that it works as described. [#]_ 

Solution
--------

The first thing we need is the spin operators. For this you can create a
`SpinOneHalfSite` which is an object in dmrg101 with the operators you
need build in: ::

    >>> from dmrg101.core.Sites import SpinOneHalfSite
    >>> left_spin = SpinOneHalfSite()
    >>> right_spin = SpinOneHalfSite()
    >>> # check all it's what you expected
    >>> print left_spin.operators['s_z']
    [[-1.  0.]
     [ 0.  1.]]
    >>> print left_spin.operators['s_p']
    [[ 0.  0.]
     [ 1.  0.]]
    >>> print left_spin.operators['s_m']
    [[ 0.  1.]
     [ 0.  0.]]

Now we have to build the Hamiltonian operator, keeping in mind the
wavefunction is a matrix. There is an `operator` object in the code which
takes care of this issue. Basically you create a new operator by creating
first a blank operator and adding to it terms. To add a term you have to
specify which is the operator acting on the left system, and which on the
right system. The following function does that:

.. literalinclude:: ./solutions/heisenberg_for_two_spins.py
    :pyobject: build_HAF_hamiltonian_for_two_spins

Then it's just a matter to call the Lanczos subroutine to solve for the
ground state and put everything together:

.. literalinclude:: ./solutions/heisenberg_for_two_spins.py
    :pyobject: main

See :download:`a full implementation of the above code
<solutions/heisenberg_for_two_spins.py>`. If you run that code you should
get something like this: 
::
    (dmrg101) $ python tutorial/solutions/heisenberg_for_two_spins.py
    The ground state energy is 0.693147.
    The ground state wavefunction is: 
    [[ 0.          0.70710678]
     [ 0.70710678  0.        ]]


.. [#] The two spin system is small enough to be solve by exact
    diagonalization, i.e. just diagonalizing fully the Hamiltonian matrix.
    We use Lanczos here, because the larger systems that we will find
    later cannot be fully diagonalized, and you're force to stick with
    Lanczos or a similar method.
