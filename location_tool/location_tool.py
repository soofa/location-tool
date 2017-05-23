import os
import importlib
import json
from functools import reduce
import numpy as np
import ast
from flask import Flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from location_tool.database import db_session
from location_tool import tasks, models, heat_map_utils as hmu

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
    bounding_boxes = db_session.query(models.BoundingBox).\
            order_by(models.BoundingBox.name).\
            filter(models.BoundingBox.state == 'ready').\
            all()
    return render_template('HeatMap.html', bounding_boxes=bounding_boxes)

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
    raw_coordinates = fields['coordinates']
    coordinates = hmu.transform_coordinates(raw_coordinates)
    samples = hmu.prepare_query(coordinates)
    fields['coordinates'] = str(coordinates)
    fields['samples'] = str(samples)
    bounding_box = models.BoundingBox(state='processing', **fields)
    try:
        db_session.add(bounding_box)
        db_session.commit()
        tasks.get_google_data.delay(bounding_box.id)
        return json.dumps({
            'name': bounding_box.name,
            'created_at': bounding_box.created_at.strftime('%Y-%m-%d'),
            'state': bounding_box.state
        }), 201
    except Exception as exc:
        print(exc)
        return json.dumps({}), 422

@app.route('/bounding-boxes/<bounding_box_id>')
def bounding_box_js(bounding_box_id):
    try:
        bounding_box = db_session.query(models.BoundingBox).\
                filter(models.BoundingBox.id == int(bounding_box_id)).\
                filter(models.BoundingBox.state == 'ready').\
                first()
    except:
        if bounding_box_id == 'default':
            return app.send_static_file('DataFiles/SoofaDataCambridge.js')
        else:
            return "", 404

    try:
        coordinates = ast.literal_eval(bounding_box.coordinates)
        samples = ast.literal_eval(bounding_box.samples)
        list_googlescores = ast.literal_eval(bounding_box.googlescores)
        googlescores = {
            tag: np.asarray(scores) for tag, scores in list_googlescores.items()
        }
        googletags = ast.literal_eval(bounding_box.googletags)
        xvals = np.asarray(samples['xvals'])
        yvals = np.asarray(samples['yvals'])
        num_xsamples = int(samples['num_xsamples'])
        num_ysamples = int(samples['num_ysamples'])

        outputgoogle = hmu.javascriptwriter(
            googlescores,
            xvals,
            yvals,
            num_xsamples,
            num_ysamples,
            googletags
        )

        #TODO: create data fetch tasks for yelp and walkscore
        fakeData = ",".join([
            "{{ lat : {lat}, lng: {lng}, count: 0 }}".format(
                lat=lat, lng=lng
            ) for lat in yvals for lng in xvals])

        outputyelp = """
        var yelpfoodData = {max: 0, data: [%s]};
        var yelpshoppingData = {max: 0, data: [%s]};
        var yelpcommunityData= {max: 0, data: [%s]};
        """ % (fakeData, fakeData, fakeData)

        outputwalkscore = """
        var walkscoreData = {max: 0, data: [%s]};
        """ % (fakeData)

        #AllScores = [yelpscores, walkscores, googlescores]
        AllScores = [googlescores]
        AllResults = []

        for score in AllScores:
            AllResults.extend(score.values())

        AvgResult = reduce((lambda x, y: np.add(x,y)), AllResults)
        AvgScore = {'averageData': AvgResult/len(AllResults)}
        AvgTags = {'averageData' : []}
        averageData = hmu.javascriptwriter(
            AvgScore,
            xvals,
            yvals,
            num_xsamples,
            num_ysamples,
            AvgTags
        )

        javascript_data = """
        {}
        {}
        {}
        {}

        var lat = {};
        var lng = {};

        var AllScores = {{"googlefood": googlefoodData, "googlecommunity": googlecommunityData, "googlebigshops": googlebigshopsData, "googlesmallshops": googlesmallshopsData, "googletourist": googletouristData, "googletransit": googletransitData, "yelpfood": yelpfoodData, "yelpshopping": yelpshoppingData, "yelpcommunity": yelpcommunityData, "walkscore": walkscoreData, "average": averageData}};

        var northeastcoord = [{}, {}];
        var southwestcoord = [{}, {}];
        """.format(
            outputyelp,
            outputwalkscore,
            outputgoogle,
            averageData,
            coordinates['center']['lat'],
            coordinates['center']['lng'],
            coordinates['northeast']['lat'],
            coordinates['northeast']['lng'],
            coordinates['southwest']['lat'],
            coordinates['southwest']['lng']
        )
        return javascript_data, 200
    except Exception as exc:
        print(exc)
        return "", 422
