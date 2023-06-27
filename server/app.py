#!/usr/bin/env python3

# we'll use these later...
# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt(app)
# bcrypt.generate_password_hash(some_password_string).decode('utf-8')
# bcrypt.check_password_hash(hashed_password_in_your_db, posted_password_to_check_against)

from flask import Flask, request, session
from flask_migrate import Migrate

from models import db, User

app = Flask(__name__)
app.secret_key = 'iamasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


# USER SIGNUP #

@app.post('/users')
def create_user():
    json = request.json
    new_user = User(username=json['username'])
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict(), 201



# SESSION LOGIN/LOGOUT#

@app.post('/login')
def login():
    pass


# EXAMPLE OTHER RESOURCES WITH AUTH #

@app.get('/cartoons')
def get_cartoons():
    return [
        { 'id': 1, 'name': 'Teenage Mutant Ninja Turtles' },
        { 'id': 2, 'name': 'Powerpuff Girls' },
        { 'id': 3, 'name': 'Thunder Cats' }
    ], 200


# APP RUN #

if __name__ == '__main__':
    app.run(port=5000, debug=True)
