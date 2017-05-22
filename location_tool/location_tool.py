import os
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from location_tool.database import db_session
from location_tool import tasks

app = Flask(__name__)
app.config.from_object('config.default')
if os.environ.get('APP_CONFIG_FILE') is not None:
    app.config.from_envvar('APP_CONFIG_FILE')
else:
    app.config.from_object('config.development')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def home_page():
    return render_template('HomePage.html')

@app.route('/heat-maps')
def heat_maps():
    return render_template('HeatMap.html')

@app.route('/bounding-box-entry')
def bounding_box_entry():
    return render_template('BoundingBox.html')
