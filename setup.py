from disutils.core import setup
from dmrg101.version import __version__

setup(name='dmrg101',
		version=__version__,
		description='Pedagogical implementation of the DMRG
		algorithm',
		author='Ivan Gonzalez',
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
		packages = ['dmrg101'],
		requires = [],
		py_modules=['dmrg101'],
		)
