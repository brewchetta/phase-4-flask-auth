#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()

import os

from flask import Flask, jsonify, request, session, render_template
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# from flask_cors import CORS

from models import db, User, Note

app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRESQL_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

URL_PREFIX = '/api/v1'

# HELPER METHODS #

def current_user():
    return User.query.filter(User.id == session.get('user_id')).first()

def check_admin():
    return current_user() and current_user().username == "chett2"


# USER SIGNUP #

@app.route('/')
@app.route('/<int:id>')
def index(id=0):
    return render_template("index.html")

@app.post(URL_PREFIX + '/users')
def create_user():
    try:
        json = request.json

        pw_hash = bcrypt.generate_password_hash(json['password']).decode('utf-8')
        new_user = User(username=json['username'], password_hash=pw_hash)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        return new_user.to_dict(), 201

    except Exception as e:
        return { 'error': str(e) }, 406


# SESSION LOGIN/LOGOUT#

@app.post(URL_PREFIX + '/login')
def login():
    json_data = request.json
    print(session.get('user_id'))
    user = User.query.filter(User.username == json_data['username']).first()

    if user and bcrypt.check_password_hash( user.password_hash, json_data['password'] ):
        session["user_id"] = user.id
        return user.to_dict(), 202

    else:
        return jsonify( {"message": "Invalid username or password"} ), 401


@app.get(URL_PREFIX + '/check_session')
def check_session():
    user = current_user()
    if user:
        return jsonify( user.to_dict() ), 200
    else:
        return {}, 400


@app.delete(URL_PREFIX + '/logout')
def logout():
    session.pop('user_id')
    return {}, 204


# EXAMPLE OTHER RESOURCES #

@app.get(URL_PREFIX + '/notes')
def get_notes():
    if check_admin():
        return jsonify( [ note.to_dict() for note in current_user().notes ] ), 200
    else:
        return "Not allowed to do that", 401

@app.post(URL_PREFIX + '/notes')
def create_note():
    try:
        data = request.json
        new_note = Note(**data)
        new_note.user = current_user()
        db.session.add(new_note)
        db.session.commit()
        return jsonify( new_note.to_dict() ), 201
    except Exception as e:
        return jsonify( {'error': str(e)} ), 406

# APP RUN #

if __name__ == '__main__':
    app.run(port=5555, debug=True)
