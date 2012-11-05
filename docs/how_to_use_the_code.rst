.. How to use the code for users.

How to use the code
===================

If you don't know what to do, we suggest you check out some of the
exercices for the school. This just describes the organization of the
code and how to do very basic stuff.

Core and utils modules
----------------------

Basically you can use the functions in the code by importing whatever you
need to your python environment. The module where the dmrg101 code lives
is called ``dmrg101.core``.

For example, the following line will make all the current python session:
 ::

        >>> from dmrg101.core import *

There is a second module with some related stuff like helpers not directly
related to the DMRG algorithm. You can import it doing:
 ::

        >>> from dmrg101.utils import *

A quick example
---------------

The following code implements the Heisenberg model for a chain of spins
1/2.

.. literalinclude:: ../tutorial/solutions/heisenberg_chain.py
