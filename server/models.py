from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(1024), nullable=False, default="https://mblogthumb-phinf.pstatic.net/MjAyMDExMDFfMTgy/MDAxNjA0MjI4ODc1NDMw.Ex906Mv9nnPEZGCh4SREknadZvzMO8LyDzGOHMKPdwAg.ZAmE6pU5lhEdeOUsPdxg8-gOuZrq_ipJ5VhqaViubI4g.JPEG.gambasg/%EC%9C%A0%ED%8A%9C%EB%B8%8C_%EA%B8%B0%EB%B3%B8%ED%94%84%EB%A1%9C%ED%95%84_%ED%95%98%EB%8A%98%EC%83%89.jpg?type=w800")
    point = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.nickname

class Trash(db.Model):
    __tablename__ = "wastes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    disposal_method = db.Column(db.Text(), nullable=False)
    image = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Trash %r>' % self.name
    
class Point(db.Model):
    __tablename__ = "point"

    id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lng = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    time = db.Column(db.Text, nullable=False)

    user = db.relationship("User")

#     @staticmethod
#     def current_time():
#         return datetime.now(pytz.timezone('Asia/Seoul'))

# seoul_time = Point.current_time()