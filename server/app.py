#!/usr/bin/env python3

from flask import Flask, request, session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from models import db, User

app = Flask(__name__)
app.secret_key = 'iamasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)


# USER SIGNUP #

@app.post('/users')
def create_user():
    json = request.json
    incoming_password = json['password']
    hashed_password = bcrypt.generate_password_hash(incoming_password).decode('utf-8')
    new_user = User( username=json['username'], password_hash=hashed_password )
    session['user_id'] = new_user.id
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict(), 201



# SESSION LOGIN/LOGOUT#

@app.post('/login')
def login():
    json = request.json
    user = User.query.filter(User.username == json['username']).first()
    if user and bcrypt.check_password_hash( user.password_hash, json['password'] ):
        session['user_id'] = user.id
        return user.to_dict(), 200
    else:
        return { 'error': 'Invalid username or password' }, 401


@app.get('/check_session')
def check_session():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user:
        return user.to_dict(), 200
    else:
        return {"message": "Not logged in"}, 401



@app.delete('/logout')
def logout():
    session['user_id'] = None
    return {"message": "Successfully logged out"}, 200


# EXAMPLE OTHER RESOURCES WITH AUTH #

@app.get('/cartoons')
def get_cartoons():
    user = User.query.filter(User.id == session.get('user_id')).first()
    if user and user.username == "Freddie":
        return [
            { 'id': 1, 'name': 'Teenage Mutant Ninja Turtles' },
            { 'id': 2, 'name': 'Powerpuff Girls' },
            { 'id': 3, 'name': 'Thunder Cats' }
        ], 200
    else:
        return { 'message': "Not authorized" }, 401


# APP RUN #

if __name__ == '__main__':
    app.run(port=5000, debug=True)
