from flask import Flask
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
