#from flask import Flask, jsonify
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
    return '''<h1>SPOTIFY, but without music streaming</h1>
<p>A prototype API for delivering track, playlist, and user data.</p>'''

@app.route('/api/resources/tracks/all', methods=['GET'])
def all_tracks():
    all_tracks = queries.all_tracks()
    return list(all_tracks)


#@app.route('/', methods=['GET','POST'])
#def index():
#        if(request.method == 'POST'):
 #           some_json = request.get_json()
  #          return jsonify({'you sent': some_json}),201
   #     else:
    #        return jsonify({'you sent': "Hello World"}),201

#@app.route('/multi/<int:num>', methods=['GET'])
#def get_multiply10(num):
#    return jsonify({'result': num*10})
