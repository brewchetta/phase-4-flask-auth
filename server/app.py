#!/usr/bin/env python3

from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from models import db, User, Note

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

URL_PREFIX = '/api/v1'

# HELPER METHODS #

# something will go here later

# USER SIGNUP #

@app.post(URL_PREFIX + '/users')
def create_user():
    try:
        data = request.json
        password_hash = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        new_user = User(
            username=data['username'], 
            password_hash=password_hash
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 406


# SESSION LOGIN/LOGOUT#

@app.post(URL_PREFIX + '/login')
def login():
    data = request.json
    user = User.query.filter(User.username == data['username']).first()
    data['password']

    if user and bcrypt.check_password_hash(user.password_hash, data["password"]):
        return user.to_dict(), 202
    else:
        return { "error": "Invalid username or password" }, 401


# EXAMPLE OTHER RESOURCES #

@app.get(URL_PREFIX + '/notes')
def get_notes():
    return jsonify( [note.to_dict() for note in Note.query.all()] ), 200

@app.post(URL_PREFIX + '/notes')
def create_note():
    try:
        data = request.json
        new_note = Note(**data)
        db.session.add(new_note)
        db.session.commit()
        return jsonify( new_note.to_dict() ), 201
    except Exception as e:
        return jsonify( {'error': str(e)} ), 406

# APP RUN #

if __name__ == '__main__':
    app.run(port=5555, debug=True)
