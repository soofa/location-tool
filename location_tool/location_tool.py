import os
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from location_tool.database import init_db, db_session

app = Flask(__name__)
app.config.from_object('config.default')
if os.environ.get('APP_CONFIG_FILE') is not None:
    app.config.from_envvar('APP_CONFIG_FILE')
else:
    app.config.from_object('config.development')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def location_tool():
    return render_template('HeatMap.html')
