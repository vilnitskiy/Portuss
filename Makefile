MANAGE=python manage.py
flake8=flake8 --exclude '*migrations*',manage.py
TEST_APP=syncapp

init:
	$(MANAGE) migrate
run:
	$(MANAGE) runserver
pyclean:
	find . -name '*.pyc' -delete
test:
	$(flake8)
	$(MANAGE) test $(TEST_APP)
test_only:
	$(MANAGE) test $(TEST_APP)
