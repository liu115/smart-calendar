# Smart Calendar 

(Lack of description)

## Requirement

- npm
- python3
- django

## Setup

### Setup python environment
```
# Install virtualenv
pip install virtualenv

# Setup virtual python env
virtualenv ENV --python=python3

cd smart-calendar
source ENV/bin/activate
pip install -r requirements.txt
```

### Setup frontend environment

You need to install `npm` for javascript packages.

```
npm install -g bower
bower install
```

### Setup database

Currently, we are using **sqlite3** as our database.

```
python manage.py migrate
```

This will generate a file `db.sqlite3`.
### Run server

```
python manage.py runserver
```
You can see the result in `http://127.0.0.1:8000/`.

