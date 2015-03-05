.PHONY: deploy test

test:
	python manage.py test

deploy: test
	git push origin master
	git push heroku master
