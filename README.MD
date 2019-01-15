[![N|Solid](https://www.drupal.org/files/issues/ddocs-3.gif)](https://docs.google.com/spreadsheets/d/1INSlOjEKIf4q_UXiSpsn_lKb8VHZKI3XWxlIkIAOawM/edit#gid=0)

Engineering Application
================

Application for setting up Risks and assigning dynamic fields

Python 2.7
---------

Install Python 3.0 from [Python download page](https://www.python.org/downloads/)

Install Dependencies
---------------------

	pip install django
	pip install pyodbc
	pip install pycrypto

Usage
-----------
	python manage.py runserver
	
First Time Deployment
----------------------
To run the application for the first time after cloning:

	#make migrations
	python manage.py makemigrations

	#apply migrations
	python manage.py migrate

	#load initial default data (loaded in fixture.json file)
	python manage.py loaddata fixture

	#runserver
	python manage.py runserver

	
Tests
-----------
Install required plugins for testing

	pip install pytest
	pip install pytest-django
	pip install git+git://github.com/mverteuil/pytest-ipdb.git
	pip install pytest-cov
	pip install mixer
	
Run the tests
---------------
	py.test
 