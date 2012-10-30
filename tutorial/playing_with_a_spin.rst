Playing with a spin
===================

The goal of this exercise is to build the wavefunction of a single spin
one-half (a.k.a. a qubit), and calculate its entanglement entropy. This is
a pretty trivial exercises that you could do without much hassle in a
piece of paper (see below.) The purpose of the exercise is just get you
familiar with how things are done in the code before moving to bigger
adventures.

The most general wavefunction of a spin one-half is simply:

.. math::
    |phi\rangle = \cos \psi |\down_arrow\rangle + \sin \psi |\up_arrow\rangle = 
    \begin{pmatrix} \cos \psi \\ \sin\psi \end{pmatrix}

The reduced density matrix obtaning by tracing out the right spin is:

.. math::
    |phi\rangle = \cos \psi |\down_arrow\rangle + \sin \psi |\up_arrow\rangle = 
    \begin{pmatrix} \cos \psi \\ \sin\psi \end{pmatrix}

The reduced density matrix is an hermitian operator, so it can be
diagonalized. With the eigenvalues of the reduced density matrix one can
calculate various quantities that quantify entanglement, such as the Von
Neumann entanglement entropy.

Exercise 
-------- 

Calculate the entanglement entropy when you trace out one of the spins in
a general state in the spin zero subspace of a two spin one-half system.
For which of the states in the spin zero subspace is are the two spin
maximally entangled (i.e. the Von Neumann entanglement entropy is
maximal)?

Hint
----

The first thing we need to do is to write the wavefunction of the two spin
system. In dmrg101 the wavefunctions are represented as matrices instead
of vectors, which may be more familiar to you. 

The reason for that is that as in DMRG we always have to split the
physical systems (say a chain of spins, or the two spins of the problems)
in left and right subsystems, the notation with matrices is more suited.
In the dmrg101 code the rows of the matrix representing a wavefunction
correspond to states of the left subsystem, and the columns correspond to
states of the right subsystem.

For example to represent the two spin one-half system, with one spin as
left subsystem and the other as right subsystem, we need a 2x2 matrix.
Matrix elements in the first row (column) will correspond to states with
the left (right) spin down.  Matrix elements in the second row (column)
will correspond to states with the left (right) spin up. The choice of
whether the first or second row corresponds to spin down or up is
arbitrary, but once you made the choice you have to be consistent.

The following code (assume that phi was given a value at some point)
is the wavefunction for our two-spin system.


Solution
--------

The plan is the following. First we are going to create a list of
wavefunctions for a bunch of different values of phi. 


Now we are going to calculate the reduced density matrix tracing out the
right system

Conclusion
----------

It is important that you note that this is the general solution for a
system of two qubits, and that two-qubits cannot be more entangled that in
the singlet state. In system of many particles is splitted in two parts
(think in a larger chain of spins cut at some point in two), one can
always represent the relevant degrees of freedom at the cut as a set of
qubits. Then it follows from the result you just proved that the most
*economical* way of representing the entanglement across the cut is to map
the degrees of freedom of each side to a qubits and *maximally entangle*
them across the cut. Any other state to be formed with the qubits in one
side and the other, will either have less entanglement across the cut than
the one in the original degrees of freedom, or use more qubits at each
side of the cut. This is the basis of the mappings used in quantum
information methods like MPS or TNS, and you will see *maximally entangled
spins/qbits* a lot in the rest of the school.
