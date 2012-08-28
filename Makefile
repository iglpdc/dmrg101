init:
	pip install -r requirements.txt

test: 
	nosetests tests

requires:
	pip freeze > requirements.txt
