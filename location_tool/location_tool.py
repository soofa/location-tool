from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def location_tool():
    return render_template('HeatMap.html')
