init:
	pip install -r requirements.txt

test: 
	nosetests tests

requires:
	pip freeze > requirements.txt

dist:
	python setup.py sdist --formats=gztar,zip
