.PHONY: deploy test migrate

test:
	@ENVIRONMENT='TESTING' python manage.py test

deploy: test
	git push origin master
	git push heroku master

migrate:
	python manage.py makemigrations
	python manage.py migrate
	@ENVIRONMENT='TESTING' python manage.py migrate

