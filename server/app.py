#!/usr/bin/env python3

### we'll use these later... ###
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# bcrypt.generate_password_hash(password).decode('utf-8')
# bcrypt.check_password_hash(hashed_password, password)
#################################

from flask import Flask, jsonify, request, session
from flask_migrate import Migrate

from models import db, User, Note

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

URL_PREFIX = '/api'


# USER SIGNUP #

@app.post('/users')
def create_user():
    try:
        data = request.json
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201
    except Exception as e:
        return { 'error': str(e) }, 406


# SESSION LOGIN/LOGOUT#

@app.post(URL_PREFIX + '/login')
def login():
    pass


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
