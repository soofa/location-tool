from flask import Flask
app = Flask(__name__)

@app.route('/')
def location_tool():
    return 'Locations!'
