.. Getting started for users

Getting started
===============

dmrg101 is written in Python and to use it you need a Python interpreter.
If you have a Linux or MacOS computer, you have it installed already. If
you have Windows or want to install a newer version of python interpreter
(not recommended, see *Which version of Python?* below) you can `get it here
<http://www.python.org/getit>`_.

Other than that you just need to install an additional python package,
virtualenv, and grab the code from our public repository. Details follow.

.. _which_version_of_python
Which version of Python?
------------------------

Once you have Python [#]_ installed, you can check which version you
have by doing [#]_: ::

        $ python --version

You need a 2.x version. Python has gone thru a major overhaul from
versions 3.x and above, and some of the libraries we use for dmrg101 do
not work fine in Python 3.x. If you don't have the required version, read
the next point.

What if I don't have the required version of Python?
----------------------------------------------------

Do nothing! Unless you know very well what are you doing, do **not**
install a new version of the interpreter from scratch. Python is used in
your computer for a whole bunch of things and upgrading by brute force
will surely break something. Fortunately we can workaround this by
creating a virtual enviroment with the python package virtualenv.

What is virtualenv?
-------------------

virtualenv is a python package that allows you to isolate a Python
distribution in a given directory of your hard drive, a virtual
enviroment. Once this virtual enviroment is activated, you can install all
kinds of python packages and even a different version of the python
interpreter itself, without interfering with your system-wide python
distribution. Once you're done using your virtual enviroment you can
simply delete it. Outside your virtual enviroment your computer will be
using your system-wide python distribution, so other processes that may be
using python are not affected by the presence of your virtual enviroment.

How to install virtualenv?
--------------------------

There are three ways, depending on which and whether you have installed a
python package manager. Try them in order until one works.

        #. Using pip: ::

                   $ pip install virtualenv

        #. Using easy_install: ::

                   $ easy_install virtualenv

        #. `Grab the virtualenv.py file <https://raw.github.com/pypa/virtualenv/master/virtualenv.py>`_ and use it as: ::

                   $ python virtualenv.py

For choices 1) and 2) and depending the permission settings in your
computer, you may need to prepend ``pip`` or ``easy_install`` commands above with ``sudo``, like: ::

        $ sudo easy_install virtualenv

The first two will install virtualenv in your system. (This is always good
ito have if you plan to use Python a lot.) The third option does not
install anything, which may be also an option. 

For further information visit the  `virtualenv's webpage
<http://www.virtualenv.org/>`_.


.. creating_a_virtual_environment_for_dmrg101
Creating a virtual enviroment for drmg101
-----------------------------------------

To avoid messing with your system-wide python installation, and even if
you have an adequate version of the python interpreter, we **strongly
recommend** to create a virtual enviroment to install dmrg101. 

dmrg101 needs to install a few python packages to run. You may have some
already installed if you are a python fan, or you may want to install them
system-wide if you get hooked by python simplicity, but you can do this
later. To avoid any mess in your computer, create a virtual environment to
use with dmrg101 (you only need to do this once): ::

        $ python virtualenv.py dmrg101
        New python executable in dmrg101/bin/python
        Installing setuptools............done.
        Installing pip...............done.

Then you **need** to activate the dmrg101 enviroment, using the scripts
inside your new drmg101 directory: ::

        $ cd dmrg101
        $ source bin/activate

You will notice that your prompt (the stuff appearing befoe the ``$`` in
your console have changed and now starts by ``(dmrg101)``. This is a
reminder that your are working inside the dmrg101 virtual environmment.

.. warning:: From now on, unless stated otherwise, we assume that you are
        working inside your dmrg101 enviroment, that is you have created
        the enviroment dmrg101 and you have activated it.

.. tip:: To let you know which commands you are supposed to be executed
        from inside the dmrg101 virtual enviroment, we will write the
        prompt as ``(dmrg101) $``, instead of the regular ``$``.

When you are done using the dmrg101 code, you have to deactivate your
enviroment: ::

        (dmrg101) $ deactivate 

This will make your prompt go back to normal and any call to Python will
use your system-wide distribution. You can activate/deactivate the dmrg101
environment again at any time as many times as you want. 

If you want to get rid of all the stuff that dmrg101 will install, just
delete the dmrg101 folder. This will take back your system as it was
before.

What about getting the correct python version?
----------------------------------------------

You can ask virtualenv to use a different version of Python inside your
virtual enviroment. This does not interferes with your system-wide Python
distribution. To do that: ::

        $ virtualenv -p /usr/bin/Python2.6 dmrg101

.. You have to explain this more in detail, in particualr the fact that
        you need to have installed the other version of python for this to
        work.

Getting the dmrg101 code
------------------------

If you didn't do it yet, create and activate the dmrg101 virtual
enviroment, as described in
:ref:`creating_a_virtual_environment_for_dmrg101` ::

        $ cd dmrg101
        $ source bin/activate

Install the dmrg101 package from the dmrg101's GitHub page using ``pip``:
 ::
        
        (dmrg101) $ pip -e https://iglpdc.github.com/dmrg101/...

Install the extra packages that dmrg101 needs to work: ::

        (dmrg101) $ make install

You will see some stuff being downloaded and installed inside the
environment. Wait a bit and *you're done installing!*

.. [#] We will use *Python* and *Python interpreter* to mean the same
        thing: what happens when you type ``python`` in  a console.

.. [#] Whenever you see code to type and the ``$``symbol, means that you
        have to type this in a console in your computer. You can open a console         in Linux and MacOS open the Terminal application, and in Windows it is 
        called MS_DOS prompt or Windows command line.







