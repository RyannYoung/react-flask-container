from flask import Flask
from flask import request
import requests
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def main():
    '''The main entry point of the application'''
    data = {
        "message": "Hello World!",
        "status": "success"
    }
    return data

@app.route("/schedule")
@cross_origin()
def schedule():
    '''Schedule a scrape to the daemon'''
    scraper = request.args.get('scraper')
    
    if scraper is None:
        data = {
            "message": "No scraper specified",
            "status": "error"
        }
        return data

    req = requests.post('http://localhost:6800/schedule.json', data={'project': 'scraper', 'spider': scraper})
    print(req.text)
    return req.text
    