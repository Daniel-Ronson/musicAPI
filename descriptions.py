from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

app = flask_api.FlaskAPI(__name__)
app.config.from_envvar('APP_CONFIG')

queries = pugsql.module('queries/')
queries.connect(app.config['DATABASE_URL'])


@app.cli.command('init')
def init_db():
    with app.app_context():
        db = queries._engine.raw_connection()
        with app.open_resource('createdb.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/', methods=['GET'])
def home():
    return '''<h1>descriptions Microservice</h1>'''

@app.route('/api/resources/descriptions', methods=['GET'])
def GetDescription():
    all_users = queries.descriptions()
    return list(descriptions)

@app.route('api/resources/descriptions', methods=['POST'])
def CreateDescription(description):
    description = request.data
    required_fields = ['description', 'username', 'url']
    description = data['description']
    username = data['username']
    url = data['url']

    query ="INSERT INTO descriptions(description, username, url) VALUES('"+description+"','"+username+"','"+url+"');"
    print(query)

    if not all([field in description for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user['id'] = queries.CreateDescription(**description)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return description, status.HTTP_201_CREATED
