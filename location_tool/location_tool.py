import os
import importlib
import json
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from location_tool.database import db_session
from location_tool import tasks, models

if os.environ.get('APP_ENVIRONMENT') is not None:
    config_module = importlib.import_module(os.environ.get('APP_ENVIRONMENT'))
else:
    config_module = importlib.import_module('config.development')

app = Flask(__name__)
app.config.from_object(config_module)


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
    bounding_boxes = db_session.query(models.BoundingBox).\
            order_by(models.BoundingBox.created_at.desc()).\
            limit(10).\
            all()
    return render_template('BoundingBox.html', bounding_boxes=bounding_boxes)

@app.route('/bounding-boxes', methods=['POST'])
def bounding_boxes():
    fields = request.get_json()
    bounding_box = models.BoundingBox(state='processing', **fields)
    try:
        db_session.add(bounding_box)
        db_session.commit()
        return json.dumps({
            'name': bounding_box.name,
            'created_at': bounding_box.created_at.strftime('%Y-%m-%d'),
            'state': bounding_box.state
        }), 201
    except:
        return json.dumps({}), 422
