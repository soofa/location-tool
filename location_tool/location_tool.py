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
        tasks.get_google_data.delay(bounding_box.id)
        return json.dumps({
            'name': bounding_box.name,
            'created_at': bounding_box.created_at.strftime('%Y-%m-%d'),
            'state': bounding_box.state
        }), 201
    except:
        return json.dumps({}), 422

@app.route('/bounding-boxes/<int:id>')
def bounding_box_js(bounding_box_id):
    try:
        bounding_box = db_session.query(models.BoundingBox).get(bounding_box_id)

        if bounding_box.output_google is not None:
            output_google = bounding_box.output_google
            AllScores.append()
        else:
            output_google = """
            var googlefoodData = {max: 0, data: []};
            var googlecommunityData = {max: 0, data: []};
            var googlebigshopsData = {max: 0, data: []};
            var googlesmallshopsData = {max: 0, data: []};
            var googletransitData = {max: 0, data: []};
            var googletouristData = {max: 0, data: []};
            """

        output_yelp = """
        var yelpfoodData = {max: 0, data: []};
        var yelpshoppingData = {max: 0, data: []};
        var yelpcommunityData= {max: 0, data: []};
        """

        output_walkscore = """
        var walkscoreData = {max: 0, data: []};
        """

        AllScores = [yelpscores, walkscores, googlescores]
        AllResults = []

        for score in AllScores:
            AllResults.extend(score.values())

        AvgResult = reduce((lambda x, y: np.add(x,y)), AllResults)
        AvgScore = {'averageData': AvgResult/len(AllResults)}
        AvgTags = {'averageData' : []}
        averageData = javascriptwriter(AvgScore, xvals, yvals, num_xsamples, num_ysamples, AvgTags)

        javascript_data = ""
        f.write(outputyelp + '\n')
        f.write(outputwalkscore + '\n')
        f.write(averageData + '\n')
        f.write(outputgoogle + '\n')
        f.write('var lat = ' + str(center_coord['lat']) + '\n')
        f.write('var lng = ' + str(center_coord['lng']) + '\n')
        f.write('var AllScores = {"googlefood": googlefoodData, "googlecommunity": googlecommunityData, "googlebigshops": googlebigshopsData, "googlesmallshops": googlesmallshopsData, "googletourist": googletouristData, "googletransit": googletransitData, "yelpfood": yelpfoodData, "yelpshopping": yelpshoppingData, "yelpcommunity": yelpcommunityData, "walkscore": walkscoreData, "average": averageData};' + '\n')
        f.write('var northeastcoord = [' + str(northeast_coord['lat']) + ',' + str(northeast_coord['lng']) + ']; \n')
        f.write('var southwestcoord = [' + str(southwest_coord['lat']) +  ',' + str(southwest_coord['lng']) + ']; \n')
    except:
        return json.dumps({}), 404
