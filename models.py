import json
import os
from pathlib import Path
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Integer, String, create_engine
from flask_migrate import Migrate

load_dotenv()
#fetch db credentials from .env file
dbusr=os.getenv('DBUSR')
dbpw=os.getenv('DBPW')
database_name = 'casting_agency'

#database_path = 'postgresql://{}:{}@{}/{}'.format(dbusr,dbpw,'localhost:5432', database_name)
uri = os.getenv('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()
migrate = Migrate()
"""
setup_db(app)
"""
def setup_db(app, database_path=uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()

"""
Movies

"""
class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = Column(db.String, nullable=False)
    releasedate = Column(db.Date, nullable=False)
    genre = Column(db.String)

    def __init__(self, title, releasedate, genre):
        self.title = title
        self.releasedate = releasedate
        self.genre = genre

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'releasedate': self.releasedate,
            'genre': self.genre
            }

"""
Actors 

"""
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    age = Column(db.Integer, nullable=False)
    gender=Column(db.String, nullable=False)


    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }