.PHONY: install 
install:
	pip install -r requirements.txt

.PHONY: test requires doc dist
test: 
	nosetests tests

requires:
	pip freeze > requirements.txt

doc: 	
	echo "making the docs"

dist:
	python setup.py sdist --formats=gztar,zip

.PHONY : all
all:	test doc requires dist

