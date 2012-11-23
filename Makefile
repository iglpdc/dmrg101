# 
# Users can install all the code, including the docs and all dependencies
# needed, by doing:
#
# 	$ make install
#
.PHONY: install 
install:
	pip install -r requirements.txt

# 
# The following are intended for developers only, you don't need to use
# them if just want to work with the codes. Target 'all' builds a python
# distribution in one shot, performing the tests, creating all the
# documentation, making a requirement file for pip, and finally packing
# all together in a python distribution that you can tag and upload to
# github.
#
.PHONY: test requires doc api-doc dist clean
test: 
	nosetests tests
	nosetests --with-doctest --doctest-options='+ELLIPSIS'

requires:
	pip freeze > requirements.txt

api-doc:
	sphinx-apidoc -o docs/ref dmrg101/

doc: api-doc 	
	cd docs && make html && cd ..

dist:
	python setup.py sdist --formats=gztar,zip

clean:
	rm docs/ref/*rst

.PHONY : all
all:	test doc requires dist
