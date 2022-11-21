from flask import Flask, jsonify, request, make_response, Response
import pandas as pd
import json
from flask_cors import CORS


urls = ["https://github.com/golang/go",
        "https://github.com/google/go-github",
        "https://github.com/angular/material",
        "https://github.com/angular/angular-cli",
        "https://github.com/sebholstein/angular-google-maps",
        "https://github.com/d3/d3",
        "https://github.com/facebook/react",
        "https://github.com/tensorflow/tensorflow",
        "https://github.com/keras-team/keras",
        "https://github.com/pallets/flask"]

app = Flask(__name__)
CORS(app, origins="*")

# home url if the api is working
@app.route('/', methods=['GET'])
def home():
    return jsonify({'data': 'working'})

# data route to get all star and fork data from database
@app.route('/data', methods=['GET'])
def data():
    data = pd.read_csv("./issue_data/all_url_star_fork.csv")
    json_data = json.loads(data.to_json(orient="records"))
    return jsonify({'data': json_data})

# data route to get all urls data
@app.route('/allUrl', methods=['GET'])
def allUrl():
    return jsonify({'data': urls})

# get data from respective repo depending upon the org and repo params
@app.route('/data/<string:org>/<string:repo>', methods=['GET'])
def disp(org, repo):
    data = pd.read_csv(
        f"./issue_data/{org}-{repo}.csv")
    json_data = json.loads(data.to_json(orient="records"))
    return jsonify({'data': json_data})


# driver function
if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0") # host on localhost and port 8000
    
