====
FAQs
====

How can I install Python?
-------------------------

If you don't have *any* version of Python installed, you can download one
at the `Python's official website <http://www.python.org>`. Be sure to
download a 2.x (e.g. 2.7.3) version, and not a 3.x (e.g. 3.3.0) version. 

If you have already *any* version of Python installed (even if it's a 3.x
version) **do not** install another. Instead follow the instructions on 
`What if I don't have the required version of Python?`.

Which version of Python do I have installed?
--------------------------------------------

If you have Python [#]_ installed, you can check which version you
have by doing [#]_: ::

        $ python --version

You need a supported version. Python has gone thru a major overhaul from
versions 3.x and above, and some of the libraries we use for dmrg101 may
not work fine in Python 3.x. If you don't have the required version,
follow the instructions on `What if I don't have the required version of
Python?`.

Which versions of Python are supported?
---------------------------------------

Any version larger than 2.4.x, and smaller that 3.x.

.. warning:: This may change with the final release of the code. So better
        wait.

What if I don't have the required version of Python?
----------------------------------------------------

.. note:: This applies if you have a brand-new machine that ships with Python 3.x.
    Otherwise everything will probably work, and you may not need to
    install pythonbrew_.

Do nothing! Unless you know very well what are you doing, do **not**
install a new version of the interpreter from scratch. Python is used in
your computer for a whole bunch of things and upgrading by brute force
will surely break something. Fortunately we can workaround this by
installing pythonbrew_.

pythonbrew_ is a python package that allows you to have isolated
installations of python in your home directory. The installations within
pythonbrew_ do not interfere with your system-wide Python installation, so
you can install and mess up as much as you want there without having sode
effects in other parts of your machine.

To install pythonbrew_, do: ::

        $ curl -kL http://xrl.us/pythonbrewinstall | bash

And then add this into your ~/.bashrc: ::

        [[ -s $HOME/.pythonbrew/etc/bashrc ]] && source
        $HOME/.pythonbrew/etc/bashrc

Once you have pythonbrew_ installed, install a version of python
supported by our code (say 2.7.2): ::

        $ pythonbrew install -force 2.7.2

.. warning:: This may take several minutes.

You can start using your new (and isolated) python installation by doing: ::

        $ pythonbrew switch 2.7.2
        # Switched to Python-2.7.2
        $ python --version
        2.7.2

As was said above while you are using a *pythonbrewed* python, all the
action happens inside a python installation in your home directory,
instead of your system-wide python installation. To resume normal behavior
and quit pythonbrew_ do:

        $ pythonbrew off

You can switch back to your pythonbrew installed python versions by using
the `switch` command again.

What is virtualenv?
-------------------

.. note:: pythonbrew_ has already virtualenv_ inside it. So if you are
    using pythonbrew you don't need to install virtualenv anew.

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

.. note:: pythonbrew_ has already virtualenv_ inside it. So if you are
    using pythonbrew you don't need to install virtualenv anew.

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

Creating a virtual environment for drmg101
------------------------------------------

To avoid messing with your system-wide python installation, and even if
you have an adequate version of the python interpreter, we **strongly
recommend** to create a virtual enviroment to install dmrg101. 

.. warning:: If you are using pythonbrew_ you need to create the environment after
    switching. See `Creating a virtual enviroment inside pythonbrew`.

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

----------------------------------------------------------------------------

.. [#] We will use *Python* and *Python interpreter* to mean the same thing: 
       what happens when you type ``python`` in  a console.

.. [#] Whenever you see code to type and the "$" symbol, means that you
       have to type this in a console in your computer. You can open a console         
       in Linux and MacOS open the Terminal application, and in Windows it is 
       called MS_DOS prompt or Windows command line.

