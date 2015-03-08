.PHONY: deploy test

test:
	@ENVIRONMENT='TESTING' python manage.py test

deploy: test
	git push origin master
	git push heroku master
