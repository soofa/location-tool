from flask import Flask
from flask import render_template

from location_tool.database import db_session

app = Flask(__name__)

@app.route('/')
def location_tool():
    return render_template('HeatMap.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
