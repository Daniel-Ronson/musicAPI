#from flask import Flask, jsonify
#app = Flask(__name__)

import sys
import flask_api
from flask import request, jsonify
from flask_api import status, exceptions
import pugsql

from werkzeug.security import generate_password_hash,check_password_hash


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

@app.route('/api/resources/user', methods=['GET'])
def user():
    if request.method == 'GET':
        query_paramenrs = request.args


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

@app.route('api/resources/user', methods=['POST'])
def create_user(user):
    user = request.data
    required_fields = ['username', 'password', 'firstname', 'lastname','email']
    username = data['username']
    password = data['password']
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    hashed_password = generate_password_hash(password)
    query ="INSERT INTO users(username, hashed_password, firstname, lastname, email) VALUEs('"+username+"','"+hashed_password+"', '"+firstname+"', '"+lastname+"', '"+email+"' );"
    print(query)

    if not all([field in user for field in required_fields]):
        raise exceptions.ParseError()
    try:
        user['id'] = queries.create_user(**user)
    except Exception as e:
        return { 'error': str(e) }, status.HTTP_409_CONFLICT

    return user, status.HTTP_201_CREATED

def update_user(user):
    search_by_id = ['columnName','columnValue','id']
    search_by_unique_constraint = ['columnName','columnValue','hashed_password']
    user = request.data
    to_filter = []

    if 'changeColumn' in user and 'changeValueTo' in user and 'hashed_password' in user:
        hashed_password = user['hashed_password']
        columnName = user['changeColumn']
        columnValue =user['changeValueTo']
        query = "UPDATE users SET {}=? WHERE password=?".format(columnName)
        to_filter.append(columnValue)
        to_filter.append(hashed_password)
        queries._engine.execute(query,to_filter)

    elif 'id' in user and 'username' in user:
        columnName = user['changeColumn']
        columnValue = password['changeValueTo']
        id = user['id']
        queries._engine.execute("UPDATE users SET %s=? WHERE id=?" % (columnName,),(columnValue,id))
    return user, status.HTTP_201_CREATED


#Search for users based off given parameter
def filter_users(query_parameters):
    id = query_parameters.get('id')
    username = query_parameters.get('username')
    hashed_password = query_parameters.get('hashed_password')

    query = "SELECT * FROM users WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if username:
        query += ' username=? AND'
        to_filter.append(username)
    if password:
        query += ' hashed_password=? AND'
        to_filter.append(hashed_password)
    if not (id or username or hashed_password):
        raise exceptions.NotFound()
    query = query[:-4] + ';'

    results = queries._engine.execute(query, to_filter).fetchall()

    return list(map(dict, results))
