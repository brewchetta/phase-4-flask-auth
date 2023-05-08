#!/usr/bin/env python3

from flask import Flask, request, session
from flask_migrate import Migrate

from models import db, User

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

db.init_app(app)

def authorize():
    user_id = session["user_id"]
    current_user = User.query.get(user_id)
    if not current_user:
        return { 'error': 'Not logged in' }, 401


# USER SIGNUP #

@app.post('/users')
def create_user():
    json = request.json
    pw_hash = bcrypt.generate_password_hash(json['password']).decode('utf-8')
    new_user = User(username=json['username'], password_hash=pw_hash)
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    return new_user.to_dict(), 201

@app.get('/check_session')
def check_session():
    user_id = session["user_id"]
    current_user = User.query.get(user_id)
    if current_user:
        return current_user.to_dict(), 200
    else:
        return { 'message': "You're not logged in" }, 401
    

# SESSION LOGIN/LOGOUT#

@app.post('/login')
def login():
    json = request.json
    current_user = User.query.where(User.username == json['username']).first()
    if (current_user and bcrypt.check_password_hash(current_user.password_hash, json['password'])):
        session['user_id'] = current_user.id
        return current_user.to_dict(), 201
    else:
        return { 'message': 'Invalid username or password'}, 401


@app.delete('/logout')
def logout():
    session.pop('user_id')
    return {}, 204

# EXAMPLE OTHER RESOURCES WITH AUTH #

@app.get('/cartoons')
def get_cartoons():
    authorize()
    return [
        {
            'id': 1,
            'name': "Yogi Bear"
        }
    ], 200
    
# @app.patch('/pictures/<int:id>')
# def patch_picture(id):
#     user_id = session["user_id"]
#     current_user = User.query.get(user_id)
#     pic = Picture.query.get(id)
#     if current_user and (pic in current_user.pictures):
#         do stuff make the patch
#     else:
#         not authorized buddy

# APP RUN #

if __name__ == '__main__':
    app.run(port=5000, debug=True)
