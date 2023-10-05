#!/usr/bin/env python3

from flask import Flask, jsonify, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
# from flask_cors import CORS

from models import db, User, Note

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# cors = CORS(app, resources={r"/api/*": {
#     "origins": "http://localhost:4000", 
#     "methods": ["GET", "POST"]
# }})

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
