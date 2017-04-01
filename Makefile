MANAGE=python manage.py
flake8=flake8 --exclude '*migrations*',manage.py
TEST_APP=pproject

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
mm:
	$(MANAGE) makemigrations
migrate:
	$(MANAGE) migrate
startapp:
	$(MANAGE) startapp $(name)
static:
	$(MANAGE) collectstatic
shell:
	$(MANAGE) shell

freeze:
	pip freeze | grep -v "pkg-resources" > requirements.txt

psql:
	sudo -u postgres psql
