# flask-restful-project-starter-code
My starter code for creating a new project

Console commands!

For setup
- `pipenv install && pipenv shell`
- generate secret key with `python -c 'import os; print(os.urandom(16))'` and place in config file


In the server folder:
- `export FLASK_APP=app.py`
- `export FLASK_RUN_PORT=3000`

- `flask db init` to create initial db setup

- `flask db revision --autogenerate -m 'message here!'` creates a db migration
- `flask db upgrade head`

Run app.py to start the server! ^_^
