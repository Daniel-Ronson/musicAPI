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

@app.route('/api/resources/users/all', methods=['GET'])
def all_users():
    all_users = queries.all_users()
    return list(all_users)

#GET user that matches id number
@app.route('/api/resources/users/<int:id>', methods=['GET'])
def users(id):
    return queries.user_by_id(id=id)

@app.route('/api/resources/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return filter_users(request.args)
    elif request.method == 'POST':
        return create_user(request.data)

@app.route('/api/resources/users/update', methods=['GET','PUT'])
def updates():
    if request.method == 'GET':
        return (list(queries.all_users()))
    if request.method == 'PUT':
        return update_user(request.data)

#When posting to flask api, erase trailing whitespaces,
#{"title":"Blue Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s24","arturl":"C;//song/img/s24"},{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23","arturl":"C;//song/img/s23"}
#{"title":"Yellow Submarine","album":"Yellow Submarine","artist":"The Beatles","duration":"3:20","url":"C://songs/s23","arturl":"C;//song/img/s23"}
def create_user(user):
    user = request.data
    required_fields = ['username', 'password', 'firstname', 'lastname','email']

    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user['id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return user, status.HTTP_201_CREATED

#Requires 'id' or 'artist title'
#{"changeColumn":"title","changeValueTo":"new song name", "artist": "The beatles","title":"Yellow Submarine",id":"1"}
def update_user(user):
    search_by_id = ['columnName','columnValue','id']
    search_by_unique_constraint = ['columnName','columnValue','username']
    user = request.data
    to_filter = []

#{"changeColumn":"title","changeValueTo":"Yellow Submarine", "artist": "The Beatles","title":"old song"}
    if 'changeColumn' in user and 'changeValueTo' in user and 'username' in user and 'password' in user:
        username = user['username']
        password = user['password']
        columnName = user['changeColumn']
        columnValue =user['changeValueTo']
        query = "UPDATE users SET {}=? WHERE username=? AND password=?".format(columnName)
        to_filter.append(columnValue)
        to_filter.append(username)
        to_filter.append(password)
        queries._engine.execute(query,to_filter)
#{"changeColumn":"title","changeValueTo":"Yellow Submarine","id":"2"}
    elif 'id' in user and 'username' in user:
        columnName = user['changeColumn']
        columnValue = password['changeValueTo']
        id = user['id']
        queries._engine.execute("UPDATE users SET %s=? WHERE id=?" % (columnName,),(columnValue,id))
    return user, status.HTTP_201_CREATED


#Search for track based off given parameter
def filter_users(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    password = query_parameters.get('password')
    firstname = query_parameters.get('firstname')
    #lastname = query_parameters.get('lastname')
    #email = query_parameters.get('email')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if password:
        query += ' password=? AND'
        to_filter.append(password)
    if not (id or username or password or firstname):
        raise exceptions.NotFound()
    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))
