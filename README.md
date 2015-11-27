# CallToSpeakers

## How to run this locally

1. Install and log into the local heroku tools: https://toolbelt.heroku.com/
1. Create a virtual environment with Python 3 (`virtualenv -p python3 env`) and activate it (`source ./env/bin/activate`)
2. Within your virtualenv install all required dependencies (`pip install -r requirements.txt`)
3. Copy `default.env` to `.env`, to set up default local environmental variables (`cp default.env .env`)
  * You may want to set up a your own github application (with callback url http://localhost:5000/complete/github) and
    copy the id and secret into this if you want local github auth
4. Start a local postgres server, with passwordless login for the 'postgres' user (e.g. `docker run --rm -p 5432:5432 postgres`)
5. Create a 'speakers' database on that server (`psql -h localhost -p 5432 --user postgres -c "CREATE DATABASE speakers"`)
6. Run the migrations (`python manage.py migrate`)
7. Start the app with foreman (`foreman start`)
8. Go to [localhost:5000](http://localhost:5000) to see the site

## Clone the remote database locally

[Heroku](https://devcenter.heroku.com/articles/heroku-postgres-import-export) have their own article on doing this generally.

A specific example is always nice though:

```bash
heroku pg:backups capture
curl -o latest.dump `heroku pg:backups public-url`
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U postgres -d speakers latest.dump
```