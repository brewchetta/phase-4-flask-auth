#!/usr/bin/env python3

# we'll use these later...

from flask import Flask, request, session
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
from models import db, User


app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

# AUTHORIZE #

def authorize():
    user = User.query.filter(User.id == session['user_id']).first()
    if not user:
        return { "error": "You don't have access to these resources" }, 401


# USER SIGNUP #

@app.post('/users')
def create_user():

    json = request.json

    password_digest = bcrypt.generate_password_hash(json['password']).decode('utf-8')

    new_user = User(username=json['username'], password_digest=password_digest)
    db.session.add(new_user)
    db.session.commit()
    session["user_id"] = new_user.id
    return new_user.to_dict(), 201



# SESSION LOGIN/LOGOUT#

@app.post('/login')
def login():
    json = request.json
    user = User.query.filter(User.username == json['username']).first()

    if user and bcrypt.check_password_hash(user.password_digest, json['password']):
        session["user_id"] = user.id
        return user.to_dict(), 200
    else:
        return { "error": "Invalid username or password" }, 401


@app.get('/check_session')
def check_session():
    user = User.query.filter(User.id == session.get('user_id')).first()
    if user:
        return user.to_dict(), 200
    else:
        return {"message": "No user logged in"}, 401
    
@app.delete('/logout')
def logout():
    session.pop('user_id')
    return { "message": "Logged out"}, 200


# EXAMPLE OTHER RESOURCES WITH AUTH #

@app.get('/cartoons')
def get_cartoons():
    authorize()
    return [
        { 'id': 1, 'name': 'Teenage Mutant Ninja Turtles' },
        { 'id': 2, 'name': 'Powerpuff Girls' },
        { 'id': 3, 'name': 'Thunder Cats' }
    ], 200


# APP RUN #

if __name__ == '__main__':
    app.run(port=5555, debug=True)
