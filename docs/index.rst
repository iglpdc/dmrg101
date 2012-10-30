.. dmrg101 documentation master file, created by
   sphinx-quickstart on Wed Oct 24 11:08:10 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to dmrg101's documentation!
===================================

dmrg101 is an implementation in Python of the `Density Matrix
Renormalization Group algorithm
<http://en.wikipedia.org/wiki/Density_matrix_renormalization_group>`_
(DMRG).  It is written with a pedagogical focus, and it's probably not
suitable for realistic research projects. dmrg101 was developed to be used
as a tutorial code for the `Taipei Density Matrix Renormalization Group
Winter School <http://sites.google.com/site/dmrg101/home>`_.

The present documentation describes the use of the code per-se. If you are
interested in the physics behind, how to use it to learn or teach DMRG,
you should visit `dmrg101's Github page <http://iglpdc.github.com/dmrg101>`_.

This documentation has two parts, one for users of the code and another
for developers. If you are just interested in using the code to learn
physics or following the tutorial for the school, you should read the User
Documentation. If you are also interested in modifying the code, expand
it, or just want to dig into and mess around you may want to read the
Developer Documentation.

Unless stated explicitily otherwise, all the materials are under a MIT
license, meaning pretty much that you can use it as you want. [#]_


User Documentation
------------------
.. toctree::
   :maxdepth: 2

   getting_started
   how_to_use_the_code
   faq
   support
   sponsors


Developer Documentation
-----------------------
.. toctree::
   :maxdepth: 2
   
   getting_the_code
   dev_requirements
   tests_docs_and_boring_stuff
   submit_a_bug
   reference


.. [#] I think... It's complicated enough so lawyers can make a living.
