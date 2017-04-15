from flask import Flask, render_template, Response, request
import json
from bson import json_util
from pymongo import MongoClient

app = Flask(__name__, static_url_path='', static_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/all')
def getAll():
    # connection string
    client = MongoClient('localhost', 27017)
    db = client.test

    # find or query data
    cursor = db.restaurants.find()
    result = list(cursor)


    for document in cursor:
        print(document)

    return Response(
        json.dumps(result, default=json_util.default),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )

if __name__ == '__main__':
    app.run()