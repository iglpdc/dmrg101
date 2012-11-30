#!/usr/bin/env python

from distutils.core import setup
from version import __version__

setup(name='dmrg101',
		version=__version__,
		description='Pedagogical implementation of the DMRG algorithm',
		long_description=open('README.md').read(),
		author='Ivan Gonzalez',
		author_email='iglpdc@gmail.com',
		url='https://github.com/iglpdc/dmrg101',
		license='MIT',
		classifiers=[
			'Enviroment :: Console',
			'Development Status :: 0 - Beta',
			'Intended Audience :: Developers',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: MIT license',
			'Natural language :: English',
			'Programming Language:: Python',
			'Topic :: Scientific/Engineering',
			'Topic :: Scientific/Engineering :: Physics',
			],
		packages = ['dmrg101', 'dmrg101.core',
			    'dmrg101.utils',
			    'dmrg101.utils.tridiagonal_solver',
			    'dmrg101.utils.models'],
		py_modules = ['version'],
		requires = [],
		)
