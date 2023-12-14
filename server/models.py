from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# --- USER --- #

class User(db.Model, SerializerMixin):
    # TABLE #
    __tablename__ = 'users'

    # COLUMNS #
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)

    # RELATIONSHIP #
    notes = db.relationship('Note', back_populates='user')

    # SERIALIZER #
    serialize_rules = ("-notes",)


# --- NOTES --- #

class Note(db.Model, SerializerMixin):
    # TABLE #
    __tablename__ = 'notes'

    # COLUMNS #
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # RELATIONSHIP #
    user = db.relationship('User', back_populates='notes')

    # SERIALIZER #
    serialize_rules = ("-user",)