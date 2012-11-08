.. Getting started for users
===============
Getting started
===============

dmrg101 is written in Python and to use it you need a Python interpreter.
Additionally it requires a couple of Python packages containing numerical
libraries.

If you are attending the School, and want to have everything ready for the
tutorial, please read the :ref:`Installation` page carefully.

Requirements
------------

Apart from the drgm101 code itself, you need the following software
installed in your computer: 

- Python (*which version*), 
- Numpy (*which version*),
- optional packages: matplolib, ...

You should install these requirements *prior* to get the dmrg101 code. If
you need the details on how to install them for your OS, take a look to
the :ref:`Installation` page.

Installing dmrg101 
------------------

First, you will need to install Python and the various packages required
as described in the sections above.  You will also need to download and
install `Git <http://git-scm.com/download>`__.

There are several different ways to install dmrg101, including a quick
method and a developer method.  For the developer method to access the
repository, see the `Developer Documentation`.

If you are attending the School, you just need to use the quick method
below.

.. _quick-install:

Quick installation
^^^^^^^^^^^^^^^^^^

.. note:: Depending on your setup, you may need to preface each of the ``pip ...``
    commands with ``sudo pip ...``. 

The easiest way to install dmrg101 is to use  ``pip``: ::

    $ pip install git+https://github.com/iglpdc/dmrg101.git
       
This will download and install the latest version of dmrg101. To upgrade
dmrg101 at a later date, you can run: ::

    $ pip install --upgrade git+https://github.com/iglpdc/dmrg101.git
    
*That's it!*

Testing
-------

.. todo:: write something with sense here.

To check that all is fine, you can try to run a few scripts: ::

>>> import dmrg101


